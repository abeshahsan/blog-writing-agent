from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Send

from blog_writing_agent.exceptions import (
    LLMRateLimitException,
    PlanGenerationException,
    SectionGenerationException,
)
from blog_writing_agent.io.markdown_writer import make_output_filename, write_markdown_output
from blog_writing_agent.logging_utils import get_logger
from blog_writing_agent.models import GraphState, Plan


class BlogGraphNodes:
    def __init__(self, llm_client: Any):
        self.llm = llm_client
        self.logger = get_logger(__name__)
        self.logger.debug("graph nodes initialized with llm=%s", type(llm_client).__name__)

    def orchestrator_node(self, state: GraphState) -> dict:
        try:
            self.logger.info("orchestrator started")
            self.logger.debug("planning topic=%s", state["topic"])
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
            self.logger.info("plan generated")
            self.logger.debug("plan title=%s tasks=%s", plan.blog_title, len(plan.tasks))
            return {"plan": plan}
        except Exception as exc:
            self.logger.exception("orchestrator failed")
            if "Rate limit exceeded" in str(exc):
                raise LLMRateLimitException(str(exc)) from exc
            raise PlanGenerationException(str(exc)) from exc

    def fanout_sections(self, state: GraphState):
        self.logger.debug("fanout started with tasks=%s", len(state["plan"].tasks))
        return [
            Send("worker", {"task": task, "topic": state["topic"], "plan": state["plan"]})
            for task in state["plan"].tasks
        ]

    def worker_node(self, state) -> dict:
        try:
            task = state["task"]
            topic = state["topic"]
            plan = state["plan"]
            self.logger.info("worker started")
            self.logger.debug("task_id=%s task_title=%s", task.id, task.title)

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

            self.logger.debug("worker section generated chars=%s", len(section_md))
            return {"sections": [section_md]}
        except Exception as exc:
            self.logger.exception("worker failed")
            if "Rate limit exceeded" in str(exc):
                raise LLMRateLimitException(str(exc)) from exc
            raise SectionGenerationException(str(exc)) from exc

    def reducer_node(self, state: GraphState) -> dict:
        self.logger.info("reducer started")
        title = state["plan"].blog_title
        body = "\n\n".join(state["sections"]).strip()
        final_md = f"# {title}\n\n{body}\n"
        self.logger.debug("reducer assembled sections=%s chars=%s", len(state["sections"]), len(final_md))

        filename = make_output_filename(title)
        output_path = write_markdown_output(filename, final_md)
        self.logger.info("markdown persisted")
        self.logger.debug("output_file=%s", output_path)

        return {"final": final_md}
