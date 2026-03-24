from pathlib import Path

from blog_writing_agent.graph.wiring import build_blog_graph
from blog_writing_agent.io import markdown_writer
from blog_writing_agent.models import Plan, Task


class _StructuredPlanInvoker:
    def __init__(self, plan):
        self._plan = plan

    def invoke(self, _messages):
        return self._plan


class _FakeLLM:
    def __init__(self):
        self._plan = Plan(
            blog_title="Integration Blog",
            tasks=[
                Task(id=1, title="Intro", brief="Brief 1"),
                Task(id=2, title="Details", brief="Brief 2"),
            ],
        )

    def with_structured_output(self, _schema):
        return _StructuredPlanInvoker(self._plan)

    def invoke(self, messages):
        # Worker prompt includes section title; use it to produce deterministic content.
        prompt = messages[1].content
        if "Section: Intro" in prompt:
            content = "## Intro\nHello"
        else:
            content = "## Details\nWorld"

        class _Response:
            def __init__(self, text):
                self.content = text

        return _Response(content)


def test_pipeline_end_to_end_writes_markdown(tmp_path, monkeypatch):
    monkeypatch.setattr(markdown_writer, "PROJECT_ROOT", Path(tmp_path))

    graph = build_blog_graph(llm_client=_FakeLLM())
    result = graph.invoke({"topic": "Write a blog on Self Attention", "sections": []})

    assert result["final"].startswith("# Integration Blog")
    assert "## Intro" in result["final"]
    assert "## Details" in result["final"]

    output_file = tmp_path / "outputs" / "integration_blog.md"
    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8").startswith("# Integration Blog")
