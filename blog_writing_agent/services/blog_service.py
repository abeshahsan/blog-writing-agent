from typing import cast

from blog_writing_agent.exceptions import GraphExecutionException
from blog_writing_agent.graph import build_blog_graph
from blog_writing_agent.logging_utils import get_logger
from blog_writing_agent.models import GraphState


class BlogService:
    def __init__(self, llm_client=None):
        self.logger = get_logger(__name__)
        self.logger.debug("initializing blog service")
        self.app = build_blog_graph(llm_client=llm_client)
        self.logger.debug("blog graph initialized")

    def generate_blog(self, topic: str) -> dict:
        try:
            self.logger.info("blog generation started")
            self.logger.debug("topic=%s", topic)
            input_state = cast(GraphState, {"topic": topic, "sections": []})
            result = self.app.invoke(input_state)
            self.logger.info("blog generation completed")
            return result
        except Exception as exc:
            self.logger.exception("blog generation failed")
            raise GraphExecutionException(str(exc)) from exc
