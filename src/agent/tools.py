# src/tools.py
import json
import logging

# The library provides 'scraper_class'
from google_patent_scraper import scraper_class

# Tenacity is used for resilient network requests
import tenacity
from requests.exceptions import ConnectionError, ReadTimeout

from . import prompts
import requests
from bs4 import BeautifulSoup

import logging


@tenacity.retry(
    retry=tenacity.retry_if_exception_type((ConnectionError, ReadTimeout)),
    wait=tenacity.wait_exponential(multiplier=1, min=2, max=30),
    stop=tenacity.stop_after_attempt(3),
    before_sleep=tenacity.before_sleep_log(logging.getLogger(__name__), logging.INFO)
)
def patent_search(query, max_results=5):
    """
    Search Google Patents by query and scrape details of found patents.

    Args:
        query (str): search query string
        max_results (int): max number of patents to scrape

    Returns:
        list of dict: each dict contains scraped patent data
    """
    base_url = 'https://patents.google.com/?q='
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        encoded_query = requests.utils.quote(query)
        search_url = base_url + encoded_query

        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # Find patent numbers on the search results page
        # NOTE: The CSS selector below might need adjustment if Google Patents changes HTML layout.
        # Inspect the results page to find proper selector.
        results = soup.select('search-result-item a[href*="/patent/"]')

        # Extract patent numbers from hrefs
        patent_numbers = []
        for a_tag in results:
            href = a_tag.get('href', '')
            # href example: "/patent/US1234567A/en"
            parts = href.split('/')
            if len(parts) > 2:
                patent_num = parts[2]
                patent_numbers.append(patent_num)
            if len(patent_numbers) >= max_results:
                break

        if not patent_numbers:
            logging.warning("No patents found for query: %s", query)
            return []

        # Initialize scraper instance
        scraper = scraper_class()

        scraped_patents = []

        for patent in patent_numbers:
            err, soup, url = scraper.request_single_patent(patent)
            if err == 'Success':
                data = scraper.get_scraped_data(soup, patent, url)
                scraped_patents.append(data)
            else:
                logging.warning("Failed to scrape patent %s: %s", patent, err)

        return scraped_patents

    except Exception as e:
        logging.error("An error occurred during patent search: %s", e)
        return []
    
def final_report(model, invention_text: str, search_results: list) -> str:
    """
    This tool takes the original invention and the search results,
    then calls the generative AI model with a specific prompt to generate
    the final, structured analysis report.
    """
    print("--- TOOL: Executing Final Report Generation ---")
    
    if isinstance(search_results, list):
        formatted_results = json.dumps(search_results, indent=2)
    else:
        formatted_results = str(search_results)

    final_prompt = prompts.FINAL_REPORT_PROMPT.format(
        invention_text=invention_text,
        search_results=formatted_results
    )

    print("   - Calling Gemini to write the final analysis...")
    report = model.generate_content(final_prompt).text
    
    return report