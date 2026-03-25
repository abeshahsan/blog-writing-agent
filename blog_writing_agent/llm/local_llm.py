from langchain_ollama import ChatOllama

from blog_writing_agent.exceptions import InvalidModelConfigurationException


def build_local_llm_client() -> ChatOllama:

    try:
        return ChatOllama(
            model="tinyllama",
            temperature=0.2,
            num_ctx=8192,
        )
    except Exception as exc:
        raise InvalidModelConfigurationException(str(exc)) from exc


def get_local_llm_client() -> ChatOllama:
    return build_local_llm_client()
