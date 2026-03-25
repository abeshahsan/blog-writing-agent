from pathlib import Path
import re

from blog_writing_agent.config import PROJECT_ROOT
from blog_writing_agent.exceptions import OutputWriteException
from blog_writing_agent.logging_utils import get_logger


logger = get_logger(__name__)


def make_output_filename(title: str) -> str:
    normalized = title.strip().lower().replace(" ", "_")
    # Windows-invalid characters can create malformed paths (notably ':' can create ADS).
    normalized = re.sub(r'[\\/:*?"<>|]+', "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("._")
    filename = (normalized or "untitled") + ".md"
    logger.info("generated output filename=%s from title=%s", filename, title)
    return filename


def write_markdown_output(filename: str, content: str) -> str:
    try:
        logger.info("writing markdown output")
        output_dir = PROJECT_ROOT / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        logger.debug("output_path=%s", output_path)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info("markdown output written in %s", str(output_path))
        return str(output_path)
    except Exception as exc:
        logger.exception("failed to write markdown output")
        raise OutputWriteException(str(exc)) from exc
