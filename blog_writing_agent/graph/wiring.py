from langgraph.graph import END, START, StateGraph

from blog_writing_agent.graph.nodes import BlogGraphNodes
from blog_writing_agent.llm import get_llm_client
from blog_writing_agent.models import GraphState


def build_blog_graph(llm_client=None):
    active_llm_client = llm_client or get_llm_client()
    nodes = BlogGraphNodes(active_llm_client)

    graph = StateGraph(GraphState)
    graph.add_node("orchestrator", nodes.orchestrator_node)
    graph.add_node("worker", nodes.worker_node)
    graph.add_node("reducer", nodes.reducer_node)

    graph.add_edge(START, "orchestrator")
    graph.add_conditional_edges("orchestrator", nodes.fanout_sections, ["worker"])
    graph.add_edge("worker", "reducer")
    graph.add_edge("reducer", END)

    return graph.compile()
