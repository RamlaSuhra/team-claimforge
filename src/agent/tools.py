# src/tools.py
from pypatent import Patent

def patent_search(query: str, max_results=3) -> list:
    """
    Searches for patents using the pypatent library and returns structured results.
    This is a tool that the agent can decide to call.
    """
    print(f"--- TOOL: Executing Patent Search with query: '{query}' ---")
    found_patents = []
    try:
        patant = Patant(query)
        patant.get_patents(max_page=1) # Fetch one page of results
        
        if not patant.patents:
            return "No patents found for this query."

        for patent in patant.patents[:max_results]:
            patent_details = {
                "title": patent.get('title'),
                "patent_number": patent.get('patent_number'),
                "abstract": patent.get('abstract'),
                "url": patent.get('link')
            }
            found_patents.append(patent_details)
        return found_patents
    except Exception as e:
        return f"An error occurred during patent search: {e}"

def final_report(model, invention_text: str, search_results: list) -> str:
    """
    This tool takes the original invention and the search results,
    then calls the generative AI model with a specific prompt to generate
    the final, structured analysis report.

    Args:
        model: The generative AI model instance (e.g., Gemini).
        invention_text: The full text of the user's invention disclosure.
        search_results: The list of prior art found by the patent_search tool.

    Returns:
        A string containing the formatted final report.
    """
    print("--- TOOL: Executing Final Report Generation ---")
    
    # Format the search results into a readable string for the prompt
    formatted_results = json.dumps(search_results, indent=2)

    # 1. Construct the final, detailed prompt
    final_prompt = prompts.FINAL_REPORT_PROMPT.format(
        invention_text=invention_text,
        search_results=formatted_results
    )

    # 2. Call the generative AI model to generate the report
    print("   - Calling Gemini to write the final analysis...")
    report = model.generate_content(final_prompt).text
    
    # 3. Return the generated report
    return report