import pytest

from blog_writing_agent.exceptions import (
    InvalidModelConfigurationException,
    MissingAPIKeyException,
)
from blog_writing_agent.llm import client as llm_client_module


def test_build_llm_client_raises_when_api_key_missing(monkeypatch):
    monkeypatch.setattr(llm_client_module, "OPENROUTER_API_KEY", "")

    with pytest.raises(MissingAPIKeyException):
        llm_client_module.build_llm_client()


def test_build_llm_client_wraps_provider_init_errors(monkeypatch):
    monkeypatch.setattr(llm_client_module, "OPENROUTER_API_KEY", "dummy-key")

    class FailingChatOpenRouter:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("bad config")

    monkeypatch.setattr(llm_client_module, "ChatOpenRouter", FailingChatOpenRouter)

    with pytest.raises(InvalidModelConfigurationException) as err:
        llm_client_module.build_llm_client()

    assert "bad config" in str(err.value)
