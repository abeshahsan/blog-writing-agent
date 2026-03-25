import os

from blog_writing_agent.config import ENV_MODE


def get_llm_client():

    if ENV_MODE == "production" or ENV_MODE == "test":

        from .cloud_llm import get_cloud_llm_client

        return get_cloud_llm_client()
    elif ENV_MODE == "development":
        from .local_llm import get_local_llm_client

        return get_local_llm_client()
