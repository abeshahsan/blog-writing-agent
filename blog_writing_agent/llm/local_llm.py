from langchain_ollama import ChatOllama

from blog_writing_agent.exceptions import InvalidModelConfigurationException
from blog_writing_agent.logging_utils import get_logger


LOCAL_MODEL = "qwen2.5:3b"
logger = get_logger(__name__)


def build_local_llm_client() -> ChatOllama:
    try:
        logger.info("initializing local llm client")
        logger.debug("provider=ollama model=%s temperature=%s num_ctx=%s", LOCAL_MODEL, 0.2, 8192)
        return ChatOllama(
            model=LOCAL_MODEL,
            temperature=0.2,
            num_ctx=8192,
        )
    except Exception as exc:
        logger.exception("local llm initialization failed")
        raise InvalidModelConfigurationException(str(exc)) from exc


def get_local_llm_client() -> ChatOllama:
    logger.debug("building local llm client")
    return build_local_llm_client()
