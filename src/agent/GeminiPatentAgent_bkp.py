# src/agent.py
import json
import re
import time
import logging
import os

from . import tools
from . import prompts
from . import memory
from .prompts import REACT_PLANNING_PROMPT


import tenacity
from google.api_core import exceptions as google_exceptions

class GeminiPatentAgent:
    """The core agent for handling patent analysis."""

    def __init__(self, model):
        """
        Initializes the agent.
        
        Args:
            model: An instance of a generative AI model (like Google's Gemini).
        """
        self.model = model
        self.memory = memory.AgentMemory()
        self.available_tools = {
            "search": tools.patent_search,
            "final_report": tools.final_report
        }
        # The API key is now handled directly by the tool function via an environment variable,
        # so it is no longer necessary to pass it to the agent at initialization.
        print("--- Gemini Patent Agent Initialized (using PatentsView API) ---")

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(google_exceptions.ResourceExhausted),
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=60),
        stop=tenacity.stop_after_attempt(10),
        before_sleep=tenacity.before_sleep_log(logging.getLogger(__name__), logging.INFO)
    )
    def _call_gemini(self, prompt):
        """
        A wrapper for calling the generative model.
        This method is now decorated with retry logic.
        """
        print("    - Calling Gemini API...")
        response = self.model.generate_content(prompt)
        print("    - ...API call successful.")
        return response.text


    def _parse_action(self, llm_output: str):
        """Uses regex to parse the LLM's output for an action."""
        match = re.search(r"Action:\s*?(\w+)?\s*\((.*)\)\s*$", llm_output, re.DOTALL | re.MULTILINE)
        if match:
            tool_name = match.group(1).strip()
            tool_input_str = match.group(2).strip()
            tool_input = tool_input_str.strip("'\"") if tool_input_str else None
            print(" tool_name from _parse_action is ", tool_name)
            return tool_name, tool_input
        else:
            print(" This is not a match in _parse_action and tool name is not found from LLM response!")
            print(f" LLM Output that failed to parse:\n{llm_output}")
            return None, None

    def run(self, user_input: str, max_iterations=5):
        """
        Runs the agent's core ReAct (Reason + Act) loop.
        """
        print(f"\n--- Running Agent with Input ---")

        planning_prompt = REACT_PLANNING_PROMPT.format(user_input=user_input)
        self.memory.add_entry(f"User Input: {user_input}")
        observation_results = {}

        for i in range(max_iterations):
            print(f"\n--- Iteration {i+1} ---")

            current_prompt = f"{planning_prompt}\n{self.memory.get_history()}"

            try:
                llm_response = self._call_gemini(current_prompt)
            except google_exceptions.ResourceExhausted as e:
                print("--- AGENT ERROR: API rate limit exceeded after multiple retries. Aborting. ---")
                print(f"--- Last error: {e} ---")
                return "Agent failed due to persistent API rate limiting."

            self.memory.add_entry(f"LLM Response:\n{llm_response}")
            print(llm_response)

            tool_name, tool_input = self._parse_action(llm_response)

            if tool_name in self.available_tools:
                if tool_name == "final_report" and not observation_results.get("search"):
                    no_results_entry = "Observation: The `final_report` tool cannot be called yet because no prior art has been found. You must use the `search` tool first, or try a different search query."
                    self.memory.add_entry(no_results_entry)
                    print(f"\n[GUARDRAIL ACTIVATED] {no_results_entry}")
                    continue

                tool_function = self.available_tools[tool_name]

                if tool_name == "search":
                    # The tools.patent_search function now reads the key from the environment variable itself.
                    result = tool_function(tool_input)
                    observation_results[tool_name] = result
                    observation_entry = f"Observation: Tool `{tool_name}` returned: {json.dumps(result, indent=2)}"
                    self.memory.add_entry(observation_entry)
                    print(observation_entry)

                elif tool_name == "final_report":
                    final_analysis = tool_function(
                        model=self.model,
                        invention_text=user_input,
                        search_results=observation_results.get("search", [])
                    )
                    return final_analysis
            else:
              
                return "The agent could not complete the request because it failed to choose a valid action."

        return "Agent reached maximum iterations without finishing."