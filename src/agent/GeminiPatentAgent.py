# src/agent.py
import json
import re
import logging
import tenacity

from . import tools
from . import prompts
from .memory import AgentMemory
from google.api_core import exceptions as google_exceptions


class GeminiPatentAgent:
    """
    The core agent for handling patent analysis using the ReAct pattern.
    Integrates with Google Gemini LLM and external tools for patent search and analysis.
    """

    def __init__(self, model, serpapi_api_key=None):
        # Initialize the agent with the LLM model and SerpAPI key for patent search
        self.model = model
        self.memory = AgentMemory()  # Stores conversation history
        self.serpapi_api_key = serpapi_api_key
        # Register available tools for the agent to use
        self.available_tools = {
            "patent_search": tools.patent_search,
            "final_report": tools.final_report
        }
        print("--- Gemini Patent Agent Initialized ---")

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(google_exceptions.ResourceExhausted),
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=60),
        stop=tenacity.stop_after_attempt(5),
        before_sleep=tenacity.before_sleep_log(logging.getLogger(__name__), logging.INFO)
    )
    def _call_gemini(self, prompt):
        """
        Calls the Gemini LLM with the given prompt, with retry logic for rate limits.
        """
        print("   - Calling Gemini API...")
        response = self.model.generate_content(prompt)
        print("   - ...API call successful.")
        return response.text

    def _parse_action(self, llm_output: str):
        """
        Parses the LLM's output for a <use_tool> XML-like tag.
        Extracts the tool name and its argument(s) for execution.
        """
        # Regex to extract <use_tool tool_name="...">...</use_tool> blocks
        tool_match = re.search(r"<use_tool tool_name=[\"'](.*?)[\"']>(.*?)</use_tool>", llm_output, re.DOTALL)

        if not tool_match:
            return None, None  # No tool call found

        tool_name = tool_match.group(1).strip()
        tool_content = tool_match.group(2).strip()

        if tool_name == "patent_search":
            # Return the tool name and the search query string
            return tool_name, tool_content

        elif tool_name == "final_report":
            # Return the tool name and an empty dict (final_report uses memory)
            return tool_name, {}  # Trigger final report, using memory

        return None, None

    def run(self, user_input: str, max_iterations=5):
        """
        Runs the agent's core ReAct loop for a given user input.
        Handles planning, tool selection, execution, and memory updates.
        """
        print(f"\n--- Running Agent with Input ---")
        # Format the planning prompt with the user's invention disclosure
        planning_prompt = prompts.REACT_PLANNING_PROMPT.format(user_input=user_input)
        self.memory.add_entry(f"User Input: {user_input}")
        observation_results = {}  # Stores results from tool calls

        for i in range(max_iterations):
            print(f"\n--- Iteration {i+1} ---")

            # Build the current prompt with planning and conversation history
            current_prompt = f"{planning_prompt}\n{self.memory.get_history()}"

            try:
                # Call the LLM to get the next thought/action
                llm_response = self._call_gemini(current_prompt)
            except google_exceptions.ResourceExhausted:
                print("--- AGENT ERROR: API rate limit exceeded after multiple retries. Aborting. ---")
                return "Agent failed due to persistent API rate limiting."

            self.memory.add_entry(f"LLM Response:\n{llm_response}")
            # Print only the thought process (before tool call)
            print(llm_response.split("<use_tool")[0])  # Thought process only

            # Parse the tool call from the LLM output
            tool_name, tool_args = self._parse_action(llm_response)

            if tool_name in self.available_tools:
                tool_function = self.available_tools[tool_name]

                if tool_name == "patent_search":
                    # tool_args is the query string from LLM
                    # Call patent_search(query, max_results=3, api_key)
                    result = tools.patent_search(tool_args, max_results=3, api_key=self.serpapi_api_key)
                    #result = tool_function(tool_args, max_results=3, api_key=self.serpapi_api_key)
                    observation_results[tool_name] = result

                    # Log the result or error from the tool
                    if isinstance(result, str):
                        observation_entry = f"Observation: Tool `{tool_name}` returned error: {result}"
                    else:
                        observation_entry = f"Observation: Tool `{tool_name}` returned: {json.dumps(result, indent=2)}"

                    self.memory.add_entry(observation_entry)
                    print(observation_entry)

                elif tool_name == "final_report":
                    print("\n--- Agent has decided to generate the final report. ---")
                    # Call final_report with the invention text and search results
                    final_analysis = tool_function(
                        model=self.model,
                        invention_text=user_input,
                        search_results=observation_results.get("patent_search", [])
                    )
                    return final_analysis

            else:
                return "The agent could not complete the request because it failed to choose a valid action format."

        return "Agent reached maximum iterations without finishing."
