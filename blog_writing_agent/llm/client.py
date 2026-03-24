import os

from blog_writing_agent.config import ENV_MODE


def get_llm_client():
    from .cloud_llm import get_llm_client as get_cloud_llm_client

    if ENV_MODE == "production":

        return get_cloud_llm_client()
    raise NotImplementedError(
        "LLM client not implemented for the current environment mode"
    )
