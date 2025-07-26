# src/tools.py
import json
import os
from serpapi import GoogleSearch # New import for Google Search

# Commented out the original patent_search function
# def patent_search(query: str, max_results=3) -> list:
#     """
#     Searches for patents using the pypatent library and returns structured results.
#     This is a tool that the agent can decide to call.
#     """
#     print(f"--- TOOL: Executing Patent Search with query: '{query}' ---")
#     found_patents = []
#     try:
#         search_results = Patent(query)
#         search_results.get_patents(max_page=1) # Fetch one page of results
#
#         if not search_results.patents:
#             return "No patents found for this query."
#
#         for patent in search_results.patents[:max_results]:
#             patent_details = {
#                 "title": patent.get('title'),
#                 "patent_number": patent.get('patent_number'),
#                 "abstract": patent.get('abstract'),
#                 "url": patent.get('link'),
#                 "claims": patent.get('claims'),
#                 "description": patent.get('description')
#             }
#             found_patents.append(patent_details)
#         return found_patents
#     except Exception as e:
#         return f"An error occurred during patent search: {e}"

def search(query: str, num_results=5) -> list:
    """
    Performs a Google Patents search using SerpApi and returns a list of structured patent results.
    This is a tool that the agent can decide to call.
    """
    print(f"--- TOOL: Executing Google Patents Search with query: '{query}' ---")
    try:
        params = {
            "engine": "google_patents", # CHANGED: from "google" to "google_patents"
            "q": query,
            "api_key": os.environ.get("SERPAPI_API_KEY"),
            "num": num_results
        }
        search_engine = GoogleSearch(params) # Renamed variable to avoid conflict with function name
        results = search_engine.get_dict()

        formatted_results = []
        if "organic_results" in results: # Google Patents results are still often under 'organic_results' or similar
            for result in results["organic_results"]:
                patent_details = {
                    "title": result.get("title"),
                    "link": result.get("link"),
                    "abstract": result.get("snippet"), # Snippet often serves as the abstract
                    "patent_number": result.get("patent_number"),
                    "publication_date": result.get("publication_date"),
                    "assignee": result.get("assignee"),
                    # You can add more fields if needed, e.g., inventors, filing_date
                    # "inventors": result.get("inventors"),
                    # "filing_date": result.get("filing_date"),
                }
                # Filter out None values for cleaner output
                patent_details = {k: v for k, v in patent_details.items() if v is not None}
                formatted_results.append(patent_details)
        else:
            return "No patent search results found."

        return formatted_results
    except Exception as e:
        return f"An error occurred during Google Patents search: {e}"


def final_report(model, invention_text: str, search_results: list) -> str:
    """
    This tool takes the original invention and the search results,
    then calls the generative AI model with a specific prompt to generate
    the final, structured analysis report.

    Args:
        model: The generative AI model instance (e.g., Gemini).
        invention_text: The full text of the user's invention disclosure.
        search_results: The list of prior art found by the search tool (now Google Patents).

    Returns:
        A string containing the formatted final report.
    """
    print("--- TOOL: Executing Final Report Generation ---")

    # Format the search results into a readable string for the prompt
    formatted_results = json.dumps(search_results, indent=2)

    # 1. Construct the final, detailed prompt
    final_prompt = FINAL_REPORT_PROMPT.format(
        invention_text=invention_text,
        search_results=formatted_results
    )

    # 2. Call the generative AI model to generate the report
    print("    - Calling Gemini to write the final analysis...")
    report = model.generate_content(final_prompt).text

    # 3. Return the generated report
    return report
