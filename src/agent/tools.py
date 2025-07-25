# src/tools.py
from pypatent import Patant

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

# This is a placeholder for the final response generation.
# In a real app, this might involve another AI call.
def final_report(invention_text, search_results):
    """
    This function signals the end of the process.
    The agent controller will call the actual report generator.
    """
    print("--- TOOL: Executing Final Report ---")
    # The actual report generation logic is handled by the agent
    # using the FINAL_REPORT_PROMPT. This tool is just a trigger.
    return "Final report generation initiated."