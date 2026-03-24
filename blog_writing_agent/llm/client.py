from langchain_openrouter import ChatOpenRouter
from pydantic import SecretStr

from blog_writing_agent.config import (
    MODEL_MAX_COMPLETION_TOKENS,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
)
from blog_writing_agent.exceptions import (
    InvalidModelConfigurationException,
    MissingAPIKeyException,
)


def build_llm_client() -> ChatOpenRouter:
    if not OPENROUTER_API_KEY:
        raise MissingAPIKeyException("OPENROUTER_API_KEY is missing")

    try:
        return ChatOpenRouter(
            model="openai/gpt-oss-20b:free",
            temperature=0.7,
            api_key=SecretStr(OPENROUTER_API_KEY),
            base_url=OPENROUTER_BASE_URL,
            max_completion_tokens=MODEL_MAX_COMPLETION_TOKENS,
        )
    except Exception as exc:
        raise InvalidModelConfigurationException(str(exc)) from exc


def get_llm_client() -> ChatOpenRouter:
    return build_llm_client()
