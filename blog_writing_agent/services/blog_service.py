from typing import cast

from blog_writing_agent.exceptions import GraphExecutionException
from blog_writing_agent.graph import build_blog_graph
from blog_writing_agent.models import GraphState


class BlogService:
    def __init__(self, llm_client=None):
        self.app = build_blog_graph(llm_client=llm_client)

    def generate_blog(self, topic: str) -> dict:
        try:
            input_state = cast(GraphState, {"topic": topic, "sections": []})
            return self.app.invoke(input_state)
        except Exception as exc:
            raise GraphExecutionException(str(exc)) from exc
