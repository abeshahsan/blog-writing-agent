import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from from_root import from_root


APP_LOGGER_NAME = "blog_writing_agent"


def _resolve_log_level(env_mode: str) -> int:
    if env_mode == "production":
        return logging.INFO
    return logging.DEBUG


def configure_logging(env_mode: str, log_dir: Path | None = None) -> logging.Logger:
    logs_path = log_dir or (from_root() / "logs")
    logs_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(APP_LOGGER_NAME)
    logger.handlers.clear()
    logger.propagate = False

    log_level = _resolve_log_level(env_mode)
    logger.setLevel(log_level)

    log_format = (
        "%(asctime)s | %(levelname)s | %(name)s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )
    formatter = logging.Formatter(log_format)

    file_handler = RotatingFileHandler(
        filename=logs_path / f"blog_writing_agent.{env_mode}.log",
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.info("logging configured")
    logger.debug("logger=%s env_mode=%s log_level=%s log_dir=%s", APP_LOGGER_NAME, env_mode, logging.getLevelName(log_level), logs_path)
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    if not name:
        return logging.getLogger(APP_LOGGER_NAME)
    return logging.getLogger(f"{APP_LOGGER_NAME}.{name}")
