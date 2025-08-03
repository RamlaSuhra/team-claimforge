from langgraph.graph import StateGraph
from ..nodes.llm_node import llm_node
from ..nodes.search_node import search_node
from ..nodes.final_report_node import final_report_node

def build_patent_graph():
    graph = StateGraph(dict)  # <-- Pass dict as the state schema
    graph.add_node("llm", llm_node)
    graph.add_node("search", search_node)
    graph.add_node("final_report", final_report_node)

    # Define the workflow: LLM -> Search -> Final Report
    graph.add_edge("llm", "search")
    graph.add_edge("search", "final_report")

    graph.set_entry_point("llm")
    return graph