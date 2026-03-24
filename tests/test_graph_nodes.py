import pytest

from blog_writing_agent.exceptions import (
    LLMRateLimitException,
    PlanGenerationException,
    SectionGenerationException,
)
from blog_writing_agent.graph.nodes import BlogGraphNodes
from blog_writing_agent.models import Plan, Task


class _StructuredInvoker:
    def __init__(self, result=None, error=None):
        self._result = result
        self._error = error

    def invoke(self, _messages):
        if self._error:
            raise self._error
        return self._result


class _LLMStub:
    def __init__(
        self, plan_result=None, plan_error=None, worker_result=None, worker_error=None
    ):
        self._plan_result = plan_result
        self._plan_error = plan_error
        self._worker_result = worker_result
        self._worker_error = worker_error

    def with_structured_output(self, _schema):
        return _StructuredInvoker(result=self._plan_result, error=self._plan_error)

    def invoke(self, _messages):
        if self._worker_error:
            raise self._worker_error

        class _Response:
            def __init__(self, content):
                self.content = content

        return _Response(self._worker_result)


def test_orchestrator_node_returns_plan():
    plan = Plan(blog_title="Title", tasks=[Task(id=1, title="Intro", brief="Brief")])
    nodes = BlogGraphNodes(_LLMStub(plan_result=plan))

    result = nodes.orchestrator_node({"topic": "X", "sections": []})

    assert result["plan"].blog_title == "Title"


def test_orchestrator_node_maps_rate_limit():
    nodes = BlogGraphNodes(_LLMStub(plan_error=RuntimeError("Rate limit exceeded")))

    with pytest.raises(LLMRateLimitException):
        nodes.orchestrator_node({"topic": "X", "sections": []})


def test_orchestrator_node_maps_general_error():
    nodes = BlogGraphNodes(_LLMStub(plan_error=RuntimeError("bad plan")))

    with pytest.raises(PlanGenerationException):
        nodes.orchestrator_node({"topic": "X", "sections": []})


def test_worker_node_maps_rate_limit():
    plan = Plan(blog_title="T", tasks=[])
    nodes = BlogGraphNodes(_LLMStub(worker_error=RuntimeError("Rate limit exceeded")))

    with pytest.raises(LLMRateLimitException):
        nodes.worker_node(
            {"topic": "X", "plan": plan, "task": Task(id=1, title="A", brief="B")}
        )


def test_worker_node_maps_general_error():
    plan = Plan(blog_title="T", tasks=[])
    nodes = BlogGraphNodes(_LLMStub(worker_error=RuntimeError("worker broke")))

    with pytest.raises(SectionGenerationException):
        nodes.worker_node(
            {"topic": "X", "plan": plan, "task": Task(id=1, title="A", brief="B")}
        )
