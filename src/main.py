# main.py
import os
from dotenv import load_dotenv

import google.generativeai as genai
from .agent.GeminiPatentAgent import GeminiPatentAgent


def read_invention_disclosure(file_path: str):
    """Reads the invention disclosure from a file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Invention disclosure file not found at '{file_path}'")
        return None

def main():
    load_dotenv()
    api_key = os.environ.get('GOOGLE_API_KEY')

    # For real model
    model = None
    if api_key:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-pro')
    else:
        print("[WARNING]: GOOGLE_API_KEY not set. Using DummyModel for testing.")
        class DummyModel:
            def generate_content(self, prompt):
                class Response:
                    text = "Action: search('test prior art')"
                return Response()
        model = DummyModel()

    file_path = './src/data/invention_disclosure.txt'
    invention_text = read_invention_disclosure(file_path)
    if not invention_text:
        return

    agent = GeminiPatentAgent(model)
    print("Running Gemini Patent Agent...")
    final_report = agent.run(invention_text)
    print("\n=== Final Report ===")
    print(final_report)

if __name__ == "__main__":
    main()