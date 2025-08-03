from ..tools.patent_tools import patent_search

def search_node(state):
    """
    Node that performs a patent search using the provided query.
    Expects 'tool_input' in the state dict.
    """
    query = state.get("tool_input")
    if not query:
        raise ValueError("State must contain 'tool_input' key for search.")
    result = patent_search(query)
    state["search_results"] = result
    return state