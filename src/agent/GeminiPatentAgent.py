"""
This module provides a LangGraph-based agent implementation.
"""

from .graph.patent_graph import build_patent_graph
from .memory.memory import AgentMemory
from .prompts.react_prompts import REACT_PLANNING_PROMPT

class GeminiPatentAgent:
    """
    Compatibility wrapper for the GeminiPatentAgent using the LangGraph workflow.
    """

    def __init__(self, model):
        """
        Initializes the agent with the given LLM model.
        Args:
            model: An LLM model instance with a generate_content(prompt) method.
        """
        self.model = model

    def run(self, user_input: str, max_iterations=5):
        """
        Runs the LangGraph-based patent agent workflow.
        Args:
            user_input (str): The invention disclosure or user query.
            max_iterations (int): Maximum number of workflow steps.
        Returns:
            str: The final report or a message if not completed.
        """
        memory = AgentMemory()
        memory.add_entry(f"User Input: {user_input}")

        state = {
            "user_input": user_input,
            "model": self.model,
            "prompt": REACT_PLANNING_PROMPT.format(user_input=user_input),
            "memory": memory,
            "tool_input": user_input  # For demo, pass user_input as tool_input
        }

        graph = build_patent_graph()
        compiled_graph = graph.compile()
        print("--- Running LangGraph Workflow ---")
        print(f"   - Initial State: {state}")
        result_state = compiled_graph.invoke(state) 
        final_report = result_state.get("final_report")
        if final_report:
            return final_report
        else:
            return "Agent did not produce a final report."

    def main(): 
        # Read the invention disclosure from a file
        file_path = 'invention_disclosure.txt'  # Adjust this path as needed
        invention_text = read_invention_disclosure(file_path)
        
        if not invention_text:
            return

        # Initialize the Gemini Patent Agent with the model
        agent = GeminiPatentAgent(model)

        # Run the agent with the invention disclosure
        print("Running Gemini Patent Agent...")
        final_report = agent.run(invention_text)

        # Output the final report
        print("\n=== Final Report ===")
        print(final_report)
    if __name__ == "__main__":
        main()
    # --- End of main.py ---
    # This script initializes the Gemini Patent Agent and runs it with an invention disclosure.
    # It reads the disclosure from a file, configures the model, and prints the final report.
    # Make sure to set the GOOGLE_API_KEY environment variable before running this script.
    # The script is designed to be run as a standalone application.
    # It uses the dotenv package to load environment variables from a .env file.    