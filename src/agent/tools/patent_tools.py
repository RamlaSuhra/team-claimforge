# src/tools.py
import json
import logging
import re
import requests
import os
import tenacity
from requests.exceptions import ConnectionError, ReadTimeout, ConnectTimeout, HTTPError

from ..prompts import react_prompts as prompts

def _clean_query(query: str) -> str:
    """
    Sanitizes the AI-generated query to a simple string of keywords,
    which is what the PatentsView API works best with.
    Removes special characters and redundant logical operators.
    """
    query = re.sub(r"[^\w\s]", " ", query)
    query = re.sub(r"\s+(AND|OR)\s+", " ", query, flags=re.IGNORECASE)
    query = re.sub(r"\s+", " ", query).strip()
    return query


def _should_retry_http_error(exception):
    """
    Return True if the HTTPError is a temporary server error worth retrying.
    Used by tenacity for retry logic on network errors.
    """
    return isinstance(exception, HTTPError) and exception.response.status_code in [
        502,
        503,
        504,
    ]


# Decorator for retrying network requests and handling transient errors
@tenacity.retry(
    retry=(
        tenacity.retry_if_exception_type((ConnectionError, ReadTimeout, ConnectTimeout))
        | tenacity.retry_if_exception(_should_retry_http_error)
    ),
    wait=tenacity.wait_exponential(multiplier=1, min=2, max=30),
    stop=tenacity.stop_after_attempt(3),
    before_sleep=tenacity.before_sleep_log(logging.getLogger(__name__), logging.INFO),
)
def patent_search(query: str, max_results=3) -> list:
    """
    Perform a patent search using the PatentsView API, sending the query in the URL.
    """
    print("--- TOOL: Executing PatentsView Search API (query string) ---")
    PATENTSVIEW_API_KEY = os.environ.get("PATENTSVIEW_API_KEY")
    if not PATENTSVIEW_API_KEY:
        error_msg = "Error: PatentsView API key is not set. Please set the 'PATENTSVIEW_API_KEY' environment variable."
        logging.error(error_msg)
        return error_msg

    cleaned_query = _clean_query(query)
    if not cleaned_query:
        return "Error: Patent search query is empty after cleaning."

    # Build the query and fields for the URL
    q_param = json.dumps({
        "_text_any": {
            "patent_title": cleaned_query,
            "patent_abstract": cleaned_query
        }
    })
    f_param = json.dumps([
        "patent_number",
        "patent_title",
        "patent_date",
        "patent_abstract"
    ])
    url = (
        f"https://search.patentsview.org/api/v1/patent"
        f"?q={requests.utils.quote(q_param)}"
        f"&f={requests.utils.quote(f_param)}"
        f"&o={json.dumps({'per_page': max_results})}"
    )

    headers = {
        "X-Api-Key": PATENTSVIEW_API_KEY
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("patents", [])
        if not results:
            return "No patents found for this query on PatentsView."

        print(f"   - Found {len(results)} results. Processing top {max_results}...")

        found_patents = []
        for result in results[:max_results]:
            patent_number = result.get("patent_number")
            patent_url = f"https://patents.google.com/patent/US{patent_number}" if patent_number else None

            found_patents.append({
                "title": result.get("patent_title"),
                "patent_number": patent_number,
                "publication_date": result.get("patent_date"),
                "abstract": result.get("patent_abstract"),
                "url": patent_url
            })

        return found_patents

    except Exception as e:
        logging.error(f"Error during patent search via PatentsView: {e}", exc_info=True)
        return f"An error occurred during patent search: {e}"

def final_report(model, invention_text: str, search_results: list) -> str:
    """
    This tool takes the original invention and the search results,
    then calls the generative AI model with a specific prompt to generate
    the final, structured analysis report.
    Args:
        model: The LLM model to use for report generation
        invention_text (str): The original invention disclosure
        search_results (list): List of prior art found
    Returns:
        str: The generated patentability analysis report
    """
    print("--- TOOL: Executing Final Report Generation ---")

    # Format search results for the prompt
    if isinstance(search_results, list):
        formatted_results = json.dumps(search_results, indent=2)
    else:
        formatted_results = str(search_results)

    # Build the final report prompt
    final_prompt = prompts.FINAL_REPORT_PROMPT.format(
        invention_text=invention_text, search_results=formatted_results
    )

    print("   - Calling Gemini to write the final analysis...")
    report = model.generate_content(final_prompt).text

    return report