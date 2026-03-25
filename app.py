import os
from bootstrap import bootstrap_env_mode


os.environ.setdefault("ENV_MODE", "development")
ENV_MODE = bootstrap_env_mode()

from blog_writing_agent.logging_utils import configure_logging


configure_logging(ENV_MODE)
