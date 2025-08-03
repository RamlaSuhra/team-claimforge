from ..tools.patent_tools import final_report

def final_report_node(state):
    """
    Node that generates the final report using the model, user input, and search results.
    Expects 'model', 'user_input', and 'search_results' in the state dict.
    """
    model = state.get("model")
    invention_text = state.get("user_input")
    search_results = state.get("search_results")
    if not model or not invention_text or search_results is None:
        raise ValueError("State must contain 'model', 'user_input', and 'search_results' keys.")
    report = final_report(model, invention_text, search_results)
    state["final_report"] = report
    return state