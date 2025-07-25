import os
import json
from pypatent import Patant # Import the pypatent library

# Import necessary libraries
import google.generativeai as genai
import os

# --- Configuration ---
# In a real application, you would securely manage your API key.
# For this example, you would need to set up your Google AI API key.
# genai.configure(api_key="YOUR_API_KEY")

class GeminiPatentAssistant:
    """
    A simplified, conceptual model of a Gemini AI Patent Assistant.
    """
    def __init__(self, api_key=None):
        """
        Initializes the assistant.
        In a real application, you would initialize the connection to the Gemini API here.
        """
        # if api_key:
        #     genai.configure(api_key=api_key)
        # self.model = genai.GenerativeModel('gemini-pro')
        print("--- Gemini AI Patent Assistant Initialized ---")
        print("Disclaimer: This is a conceptual script for demonstration purposes.")
        print("It does not provide legal advice and cannot approve a patent.\n")


    # --- Feature 1: Document Upload ---
    def upload_patent_document(file_path: str):
        """
        Simulates uploading a patent document by reading its content from a file.

        Args:
            file_path: The local path to the .txt file containing the invention disclosure.

        Returns:
            The text content of the file as a string, or None if the file doesn't exist.
        """
        print("--- 1. Document Upload ---")
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            print(f"Successfully loaded document: '{file_path}'")
            return content
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None

    # --- Feature 2: AI-Powered Analysis (Keyword & Concept Extraction) ---
    def analyze_invention_for_keywords(invention_text: str):
        """
        Uses a simulated AI call to analyze the invention text and extract key concepts.

        Args:
            invention_text: The full text of the invention disclosure.

        Returns:
            A query string suitable for a patent search.
        """
        print("\n--- 2. AI-Powered Analysis ---")
        print("Extracting key concepts to build a search query...")

        #
        # --- This is where you would call a real Generative AI model. ---
        #
        # PROMPT FOR GEMINI:
        # """
        # As a patent analyst, review the following invention disclosure and create
        # a concise but comprehensive search query string for use with a patent database.
        # Combine the most critical technical terms using Boolean operators like AND/OR if appropriate.
        #
        # Invention Disclosure:
        # "{invention_text}"
        # """
        #
        # --- Simulation of AI Output ---
        # The AI would identify the most critical, unique concepts.
        simulated_query = '"acoustic sensor" AND "leak detection" AND ("machine learning" OR "AI")'
        
        print(f"   - Generated Patent Search Query: {simulated_query}")
        return simulated_query

    # --- Feature 3: Comprehensive Prior Art Search using pypatent ---
    def search_for_prior_art_with_pypatent(query: str, max_results=5):
        """
        Searches for patents using the pypatent library and returns structured results.

        Args:
            query: The search query string.
            max_results: The maximum number of patents to retrieve.

        Returns:
            A list of dictionaries, where each dictionary contains details of a found patent.
        """
        print("\n--- 3. Comprehensive Prior Art Search (using pypatent) ---")
        print(f"   - Querying Google Patents with: {query}")
        
        found_patents = []
        try:
            # Initialize the Patant search object
            patant = Patant(query)
            # Fetch the patents. We set a max_results limit to keep the demo quick.
            patant.get_patents(max_page=1) # Fetching one page of results
            
            if not patant.patents:
                print("   - No patents found for this query.")
                return found_patents

            print(f"   - Found {len(patant.patents)} results. Processing top {max_results}...")

            # Process the results into a clean list
            for patent in patant.patents[:max_results]:
                patent_details = {
                    "title": patent.get('title'),
                    "patent_number": patent.get('patent_number'),
                    "publication_date": patent.get('publication_date'),
                    "abstract": patent.get('abstract'),
                    "url": patent.get('link')
                }
                found_patents.append(patent_details)
                
        except Exception as e:
            print(f"An error occurred during patent search: {e}")
            # In a real app, you might want to try a different search strategy or log the error.
            
        return found_patents


    # --- Feature 4: Novelty Assessment and Report Generation ---
    def generate_patentability_report(invention_text: str, prior_art_patents: list):
        """
        Simulates an AI generating a structured report by comparing the invention
        against the patents found by pypatent.

        Args:
            invention_text: The original invention text.
            prior_art_patents: The list of patent details from pypatent.

        Returns:
            A formatted string containing the final report.
        """
        print("\n--- 4. Generating Patentability Report ---")

        # Build the prior art section of the prompt dynamically
        prior_art_summary = ""
        if not prior_art_patents:
            prior_art_summary = "No direct patent prior art was found in the initial search."
        else:
            for i, patent in enumerate(prior_art_patents):
                prior_art_summary += f"""
        Prior Art #{i+1}:
        - Title: {patent['title']}
        - Patent Number: {patent['patent_number']}
        - Abstract: {patent['abstract']}
        ---
        """
        #
        # --- This is where the powerful AI analysis happens. ---
        #
        # PROMPT FOR GEMINI:
        # """
        # You are a patent analyst AI. Your task is to provide a preliminary patentability
        # assessment based on an invention disclosure and a list of prior art patents.
        #
        # **INVENTION DISCLOSURE:**
        # "{invention_text}"
        #
        # **PRIOR ART PATENTS:**
        # {prior_art_summary}
        #
        # **Instructions:**
        # 1.  **Overall Assessment:** Start with a high-level summary of the patentability landscape based on the abstracts of the found patents.
        # 2.  **Analysis of Novelty:** For each piece of prior art, explain how its abstract suggests it might challenge the novelty of the invention. Quote the relevant parts of the abstract.
        # 3.  **Key Distinguishing Features:** Identify what aspects of the invention disclosure appear to be novel and not explicitly mentioned in the abstracts of the prior art.
        # 4.  **Recommendation:** Conclude with a recommendation on whether to proceed and what to focus the patent claims on.
        # """
        #
        # --- Simulation of AI-Generated Report ---
        report = f"""
        ======================================================================
        ===           PRELIMINARY PATENTABILITY ASSESSMENT REPORT          ===
        ======================================================================

        **Invention Under Review:** AI-Powered Predictive Water Management System

        **1. Overall Assessment:**
        The patent search confirms that the field of using acoustic analysis for leak detection is crowded. Multiple patents explicitly combine this with computer analysis, and some mention machine learning or AI. The key to patentability will be demonstrating a specific, novel technological method within this established framework, particularly concerning the *predictive* aspect of the AI model.

        **2. Analysis of Novelty (Based on Found Patents):**
        """
        
        if not prior_art_patents:
            report += "\n    No conflicting patents were found in this search. This could indicate a higher likelihood of novelty, but a more thorough search is recommended."
        else:
            for i, patent in enumerate(prior_art_patents):
                report += f"""
        *   **Prior Art #{i+1}: {patent['patent_number']} - "{patent['title']}"**
            - **Potential Conflict:** The abstract of this patent discusses "{patent['abstract']}". This directly overlaps with the invention's use of acoustic signals and computer analysis to identify leaks. The core concept is clearly established here.
            - **URL:** {patent['url']}
        """

        report += """
        **3. Potential Distinguishing Features:**
        While the general concept is well-trodden, the provided prior art abstracts do not explicitly detail the following concepts from the invention disclosure:
        - **Predictive Analysis:** The abstracts focus on *detection* of existing leaks. The invention's claim to predict failures *before* they occur by analyzing "pipe stress" signatures remains a potentially novel feature.
        - **Self-Adhesive Wireless Sensors:** The specific form factor of the sensors (wireless, self-adhesive) might constitute a novel and non-obvious element of the system's implementation.
        - **Integrated Automated Shut-Off:** The complete, closed-loop system (sense -> predict -> alert -> shut-off) may be a novel combination if not disclosed in the full text of the prior art.

        **4. Recommendation:**
        A broad patent on "using AI to analyze acoustic sensor data for leaks" is highly unlikely to succeed. However, a more focused application has merit.

        **It is recommended to focus the patent claims on:**
        - The unique methodology of the *predictive* AI model that distinguishes it from simple detection algorithms.
        - The specific design and function of the wireless, non-invasive acoustic sensors.
        - The complete, integrated system as a novel combination of elements providing a proactive, predictive safety function.

        Further analysis of the full text of these patents is essential.

        --- END OF REPORT ---
        """
        print("   - Report successfully generated.")
        return report
    
    # --- Main Execution Block ---
if __name__ == "__main__":
    # 1. Initialize the assistant
    assistant = GeminiPatentAssistant()

    # Define the path to the invention document
    document_path = "invention_disclosure.txt"

    # Step 1: Upload the document
    invention_content = assistant.upload_patent_document(document_path)
    
    if invention_content:
                # Step 2: Analyze and create a patent search query
                search_query = assistant.analyze_invention_for_keywords(invention_content)

                # Step 3: Search for prior art using pypatent
                prior_art_patents_found = assistant.search_for_prior_art_with_pypatent(search_query, max_results=3)

                # Step 4: Generate the final report based on the pypatent results
                final_report = assistant.generate_patentability_report(invention_content, prior_art_patents_found)
                
                # Print the final, formatted report
                print(final_report)