# main.py
import google.generativeai as genai
import os
from agent.GeminiPatentAgent import GeminiPatentAgent

# --- Configuration ---
# Get your API key from environment variables or secure storage
#os.environ['GOOGLE_API_KEY'] = 
try:
    API_KEY = "AIzaSyA0zu8mHGjgHd98M2ULyL0LZJsWx_ReOFY"##os.environ['GOOGLE_API_KEY']
except KeyError:
    print("ERROR: GOOGLE_API_KEY environment variable not set.")
    exit()

genai.configure(api_key=API_KEY)
# Using a text-focused model suitable for this task
model = genai.GenerativeModel('gemini-1.5-flash')

def read_invention_disclosure(file_path: str):
    """Reads the invention disclosure from a file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Invention disclosure file not found at '{file_path}'")
        return None

if __name__ == "__main__":
    # 1. Receive User Input (by reading the file)
    invention_file = "invention_disclosure.txt"
    invention_details = read_invention_disclosure(invention_file)

    if invention_details:
        # 2. Initialize and Run the Agent
        patent_agent = GeminiPatentAgent(model=model)
        final_response = patent_agent.run(user_input=invention_details)
        
        # 5. Print the Final Response
        print("\n======================================================")
        print("===        FINAL PATENTABILITY ANALYSIS        ===")
        print("======================================================")
        print(final_response)