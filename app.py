import os
from pathlib import Path
from uuid import uuid4

from bootstrap import bootstrap_env_mode

ENV_MODE = bootstrap_env_mode()

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from starlette.background import BackgroundTask

from blog_writing_agent import BlogService
from blog_writing_agent.logging_utils import configure_logging

configure_logging(ENV_MODE)


app = FastAPI()

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"
TEMP_OUTPUT_DIR = ROOT_DIR / "outputs" / "temp"


class GenerateBlogRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=120)

    @field_validator("topic")
    @classmethod
    def validate_topic_words(cls, value: str) -> str:
        words = value.strip().split()
        if len(words) > 20:
            raise ValueError("topic must be 20 words or fewer")
        return value.strip()


def _safe_delete(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except Exception:
        # Best-effort cleanup after response has been sent.
        pass


app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/")
def read_root() -> FileResponse:
    index_file = FRONTEND_DIR / "index.html"
    return FileResponse(index_file)


@app.post("/api/generate")
def generate_blog(request: GenerateBlogRequest) -> FileResponse:
    try:
        service = BlogService()
        result = service.generate_blog(f"Write a blog on {request.topic}")
        markdown_content = result.get("final", "").strip()

        if not markdown_content:
            raise HTTPException(status_code=500, detail="Generated markdown was empty")

        TEMP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        file_path = TEMP_OUTPUT_DIR / f"generated_{uuid4().hex}.md"
        file_path.write_text(markdown_content, encoding="utf-8")

        return FileResponse(
            path=file_path,
            media_type="text/markdown; charset=utf-8",
            filename="generated_blog.md",
            background=BackgroundTask(_safe_delete, file_path),
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

