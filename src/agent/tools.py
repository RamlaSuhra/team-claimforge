# src/tools.py
import json
import logging
import re
import requests
import time
import os

# Tenacity is used for resilient network requests
import tenacity
from requests.exceptions import ConnectionError, ReadTimeout, ConnectTimeout, HTTPError

from . import prompts


def _clean_query(query: str) -> str:
    """
    Sanitizes the AI-generated query to a simple string of keywords,
    which is what the PatentsView API works best with.
    Removes special characters and redundant logical operators.
    """
    query = re.sub(r'[^\\w\s]', ' ', query)
    query = re.sub(r'\s+(AND|OR)\s+', ' ', query, flags=re.IGNORECASE)
    query = re.sub(r'\s+', ' ', query).strip()
    return query


def _should_retry_http_error(exception):
    """
    Return True if the HTTPError is a temporary server error worth retrying.
    Used by tenacity for retry logic on network errors.
    """
    return isinstance(exception, HTTPError) and exception.response.status_code in [502, 503, 504]

# Decorator for retrying network requests and handling transient errors
@tenacity.retry(
    retry=(
        tenacity.retry_if_exception_type((ConnectionError, ReadTimeout, ConnectTimeout)) |
        tenacity.retry_if_exception(_should_retry_http_error)
    ),
    wait=tenacity.wait_exponential(multiplier=1, min=2, max=30),
    stop=tenacity.stop_after_attempt(3),
    before_sleep=tenacity.before_sleep_log(logging.getLogger(__name__), logging.INFO)
)
def patent_search(query: str, max_results=3, api_key: str = None) -> list:
    """
    Perform patent search using SerpAPI's Google Patents API.
    Requires a valid SerpAPI API key.
    Args:
        query (str): The search query string (from LLM or user)
        max_results (int): Maximum number of results to return
        api_key (str): SerpAPI key for authentication
    Returns:
        list: List of found patents (dicts) or error string
    """
    api_key = os.environ['SERP_API_KEY']
    print(f"--- TOOL: Executing SerpAPI Google Patents Search ---")
    if not api_key:
        return "Error: SerpAPI requires an API key."

    params = {
        "engine": "google_patents",
        "q": query,
        "api_key": api_key
    }

    try:
        # Make the HTTP request to SerpAPI
        response = requests.get("https://serpapi.com/search", params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        results = data.get("patent_results", [])
        if not results:
            return "No patents found for this query on Google Patents (via SerpAPI)."

        print(f"   - Found {len(results)} results. Processing top {max_results}...")

        found_patents = []
        for result in results[:max_results]:
            found_patents.append({
                "title": result.get("title"),
                "patent_number": result.get("patent_id"),
                "publication_date": result.get("publication_date"),
                "abstract": result.get("snippet"),
                "url": result.get("link")
            })
        
        return found_patents

    except Exception as e:
        # Log and return error if the search fails
        logging.error(f"Error during patent search via SerpAPI: {e}", exc_info=True)
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
        invention_text=invention_text,
        search_results=formatted_results
    )

    print("   - Calling Gemini to write the final analysis...")
    report = model.generate_content(final_prompt).text
    
    return report