import pytest

from blog_writing_agent.exceptions import GraphExecutionException
from blog_writing_agent.services import blog_service as service_module


class _OkApp:
    def invoke(self, state):
        return {"final": "ok", "input": state}


class _FailApp:
    def invoke(self, state):
        raise RuntimeError("graph exploded")


def test_generate_blog_returns_graph_output(monkeypatch):
    monkeypatch.setattr(
        service_module, "build_blog_graph", lambda llm_client=None: _OkApp()
    )

    service = service_module.BlogService()
    result = service.generate_blog("topic")

    assert result["final"] == "ok"
    assert result["input"] == {"topic": "topic", "sections": []}


def test_generate_blog_wraps_graph_errors(monkeypatch):
    monkeypatch.setattr(
        service_module, "build_blog_graph", lambda llm_client=None: _FailApp()
    )

    service = service_module.BlogService()

    with pytest.raises(GraphExecutionException) as err:
        service.generate_blog("topic")

    assert "graph exploded" in str(err.value)
