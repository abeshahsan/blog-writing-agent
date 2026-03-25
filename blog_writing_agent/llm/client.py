import os

from blog_writing_agent.config import ENV_MODE
from blog_writing_agent.logging_utils import get_logger


logger = get_logger(__name__)


def get_llm_client():
    logger.info("resolving llm client")
    logger.debug("env_mode=%s", ENV_MODE)
    if ENV_MODE == "production" or ENV_MODE == "test":
        from .cloud_llm import get_cloud_llm_client

        logger.info("using cloud llm client")
        return get_cloud_llm_client()
    elif ENV_MODE == "development":
        from .local_llm import get_local_llm_client

        logger.info("using local llm client")
        return get_local_llm_client()

    logger.warning("unknown ENV_MODE, defaulting to local llm: %s", ENV_MODE)
    from .local_llm import get_local_llm_client

    return get_local_llm_client()
