import os

from from_root import from_root

from blog_writing_agent.logging_utils import get_logger

PROJECT_ROOT = from_root()

ENV_MODE = os.environ["ENV_MODE"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
OPENROUTER_BASE_URL = os.environ["OPENROUTER_BASE_URL"]
OPENROUTER_MODEL = os.environ["OPENROUTER_MODEL"]

MODEL_MAX_COMPLETION_TOKENS = 512


def log_runtime_config() -> None:
    logger = get_logger(__name__)
    logger.info("runtime configuration loaded")
    logger.info("env_mode=%s", ENV_MODE)
    logger.info("model=%s", OPENROUTER_MODEL)
    logger.debug("openrouter_base_url=%s", OPENROUTER_BASE_URL)
    logger.debug("openrouter_api_key_present=%s", bool(OPENROUTER_API_KEY))
    logger.debug("max_completion_tokens=%s", MODEL_MAX_COMPLETION_TOKENS)

__all__ = [
    "PROJECT_ROOT",
    "ENV_MODE",
    "OPENROUTER_API_KEY",
    "OPENROUTER_BASE_URL",
    "OPENROUTER_MODEL",
    "MODEL_MAX_COMPLETION_TOKENS",
    "log_runtime_config",
]
