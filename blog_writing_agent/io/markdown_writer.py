from pathlib import Path

from blog_writing_agent.config import PROJECT_ROOT
from blog_writing_agent.exceptions import OutputWriteException


def make_output_filename(title: str) -> str:
    return title.lower().replace(" ", "_") + ".md"


def write_markdown_output(filename: str, content: str) -> str:
    try:
        output_dir = PROJECT_ROOT / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return str(output_path)
    except Exception as exc:
        raise OutputWriteException(str(exc)) from exc
