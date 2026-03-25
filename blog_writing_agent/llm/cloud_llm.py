from langchain_openrouter import ChatOpenRouter
from pydantic import SecretStr

from blog_writing_agent.config import (
    MODEL_MAX_COMPLETION_TOKENS,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
)
from blog_writing_agent.exceptions import (
    InvalidModelConfigurationException,
    MissingAPIKeyException,
)
from blog_writing_agent.logging_utils import get_logger


logger = get_logger(__name__)


def build_cloud_llm_client() -> ChatOpenRouter:
    if not OPENROUTER_API_KEY:
        logger.error("cloud llm initialization failed: missing api key")
        raise MissingAPIKeyException("OPENROUTER_API_KEY is missing")

    try:
        logger.info("initializing cloud llm client")
        logger.debug(
            "provider=openrouter model=%s base_url=%s max_completion_tokens=%s",
            OPENROUTER_MODEL,
            OPENROUTER_BASE_URL,
            MODEL_MAX_COMPLETION_TOKENS,
        )
        return ChatOpenRouter(
            model=OPENROUTER_MODEL,
            temperature=0.7,
            api_key=SecretStr(OPENROUTER_API_KEY),
            base_url=OPENROUTER_BASE_URL,
            max_completion_tokens=MODEL_MAX_COMPLETION_TOKENS,
        )
    except Exception as exc:
        logger.exception("cloud llm initialization failed")
        raise InvalidModelConfigurationException(str(exc)) from exc


def get_cloud_llm_client() -> ChatOpenRouter:
    logger.debug("building cloud llm client")
    return build_cloud_llm_client()
