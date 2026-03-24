from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Send

from blog_writing_agent.exceptions import (
    LLMRateLimitException,
    PlanGenerationException,
    SectionGenerationException,
)
from blog_writing_agent.io.markdown_writer import make_output_filename, write_markdown_output
from blog_writing_agent.models import GraphState, Plan


class BlogGraphNodes:
    def __init__(self, llm_client: Any):
        self.llm = llm_client

    def orchestrator_node(self, state: GraphState) -> dict:
        try:
            plan = self.llm.with_structured_output(Plan).invoke(
                [
                    SystemMessage(
                        content=(
                            "Create a blog plan with 5-7 sections on the following topic."
                        )
                    ),
                    HumanMessage(content=f"Topic: {state['topic']}"),
                ]
            )
            return {"plan": plan}
        except Exception as exc:
            if "Rate limit exceeded" in str(exc):
                raise LLMRateLimitException(str(exc)) from exc
            raise PlanGenerationException(str(exc)) from exc

    def fanout_sections(self, state: GraphState):
        return [
            Send("worker", {"task": task, "topic": state["topic"], "plan": state["plan"]})
            for task in state["plan"].tasks
        ]

    def worker_node(self, state) -> dict:
        try:
            task = state["task"]
            topic = state["topic"]
            plan = state["plan"]

            blog_title = plan.blog_title

            section_md = self.llm.invoke(
                [
                    SystemMessage(content="Write one clean Markdown section."),
                    HumanMessage(
                        content=(
                            f"Blog: {blog_title}\n"
                            f"Topic: {topic}\n\n"
                            f"Section: {task.title}\n"
                            f"Brief: {task.brief}\n\n"
                            "Return only the section content in Markdown."
                        )
                    ),
                ]
            ).content.strip()

            return {"sections": [section_md]}
        except Exception as exc:
            if "Rate limit exceeded" in str(exc):
                raise LLMRateLimitException(str(exc)) from exc
            raise SectionGenerationException(str(exc)) from exc

    def reducer_node(self, state: GraphState) -> dict:
        title = state["plan"].blog_title
        body = "\n\n".join(state["sections"]).strip()
        final_md = f"# {title}\n\n{body}\n"

        filename = make_output_filename(title)
        write_markdown_output(filename, final_md)

        return {"final": final_md}
