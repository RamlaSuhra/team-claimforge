def llm_node(state):
    """
    Node that calls the LLM with the current prompt and updates the state with the response.
    Expects 'model' and 'prompt' in the state dict.
    """
    model = state.get("model")
    prompt = state.get("prompt")
    if not model or not prompt:
        raise ValueError("State must contain 'model' and 'prompt' keys.")
    response = model.generate_content(prompt)
    state["llm_response"] = response.text