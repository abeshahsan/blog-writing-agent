import os
from bootstrap import bootstrap_env_mode


ENV_MODE = bootstrap_env_mode()

from blog_writing_agent import BlogService
from blog_writing_agent.config import log_runtime_config
from blog_writing_agent.logging_utils import configure_logging


def main() -> None:
    logger = configure_logging(ENV_MODE)
    logger.info("starting blog writing agent")
    logger.info("using env: %s\n\n", ENV_MODE)

    log_runtime_config()

    service = BlogService()
    logger.debug("service initialized")
    result = service.generate_blog("Write a blog on Self Attention")
    logger.info("blog generated successfully")
    logger.debug("generated markdown length=%s", len(result["final"]))


if __name__ == "__main__":
    main()
