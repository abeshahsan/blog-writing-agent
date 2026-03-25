import pytest
import sys
import types

from blog_writing_agent.exceptions import (
    InvalidModelConfigurationException,
    MissingAPIKeyException,
)
from blog_writing_agent.llm import client as llm_client_module
from blog_writing_agent.llm import cloud_llm as cloud_llm_module


def test_build_cloud_llm_client_raises_when_api_key_missing(monkeypatch):
    monkeypatch.setattr(cloud_llm_module, "OPENROUTER_API_KEY", "")

    with pytest.raises(MissingAPIKeyException):
        cloud_llm_module.build_cloud_llm_client()


def test_build_cloud_llm_client_wraps_provider_init_errors(monkeypatch):
    monkeypatch.setattr(cloud_llm_module, "OPENROUTER_API_KEY", "dummy-key")

    class FailingChatOpenRouter:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("bad config")

    monkeypatch.setattr(cloud_llm_module, "ChatOpenRouter", FailingChatOpenRouter)

    with pytest.raises(InvalidModelConfigurationException) as err:
        cloud_llm_module.build_cloud_llm_client()

    assert "bad config" in str(err.value)


def test_get_llm_client_routes_to_local_in_development(monkeypatch):
    expected_client = object()
    monkeypatch.setattr(llm_client_module, "ENV_MODE", "development")

    fake_local_llm = types.SimpleNamespace(get_local_llm_client=lambda: expected_client)
    monkeypatch.setitem(sys.modules, "blog_writing_agent.llm.local_llm", fake_local_llm)

    assert llm_client_module.get_llm_client() is expected_client


def test_get_llm_client_routes_to_cloud_in_test(monkeypatch):
    expected_client = object()
    monkeypatch.setattr(llm_client_module, "ENV_MODE", "test")
    monkeypatch.setattr(cloud_llm_module, "get_cloud_llm_client", lambda: expected_client)

    assert llm_client_module.get_llm_client() is expected_client
