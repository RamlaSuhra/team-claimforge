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
    """The core agent for handling patent analysis."""

    def __init__(self, model):
        self.model = model
        self.memory = AgentMemory()
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
        print("   - Calling Gemini API...")
        response = self.model.generate_content(prompt)
        print("   - ...API call successful.")
        return response.text

    def _parse_action(self, llm_output: str):
        """Parses the LLM's output for a <use_tool> XML-like tag."""
        tool_match = re.search(r"<use_tool tool_name=[\"'](.*?)[\"']>(.*?)</use_tool>", llm_output, re.DOTALL)
        
        if not tool_match:
            return None, None

        tool_name = tool_match.group(1).strip()
        tool_content = tool_match.group(2).strip()

        if tool_name == "patent_search":
            return tool_name, tool_content

        elif tool_name == "final_report":
            return tool_name, {}  # Trigger final report, using memory

        return None, None

    def run(self, user_input: str, max_iterations=5):
        print(f"\n--- Running Agent with Input ---")
        planning_prompt = prompts.REACT_PLANNING_PROMPT.format(user_input=user_input)
        self.memory.add_entry(f"User Input: {user_input}")
        observation_results = {}
        
        for i in range(max_iterations):
            print(f"\n--- Iteration {i+1} ---")

            current_prompt = f"{planning_prompt}\n{self.memory.get_history()}"

            try:
                llm_response = self._call_gemini(current_prompt)
            except google_exceptions.ResourceExhausted:
                print("--- AGENT ERROR: API rate limit exceeded after multiple retries. Aborting. ---")
                return "Agent failed due to persistent API rate limiting."

            self.memory.add_entry(f"LLM Response:\n{llm_response}")
            print(llm_response.split("<use_tool")[0])  # Thought process only

            tool_name, tool_args = self._parse_action(llm_response)

            if tool_name in self.available_tools:
                tool_function = self.available_tools[tool_name]

                if tool_name == "patent_search":
                    result = tool_function(tool_args)
                    observation_results[tool_name] = result

                    if isinstance(result, str):
                        observation_entry = f"Observation: Tool `{tool_name}` returned error: {result}"
                    else:
                        observation_entry = f"Observation: Tool `{tool_name}` returned: {json.dumps(result, indent=2)}"
                    
                    self.memory.add_entry(observation_entry)
                    print(observation_entry)

                elif tool_name == "final_report":
                    print("\n--- Agent has decided to generate the final report. ---")
                    final_analysis = tool_function(
                        model=self.model,
                        invention_text=user_input,
                        search_results=observation_results.get("patent_search", [])
                    )
                    return final_analysis

            else:
                print("\n--- Agent did not choose a valid action. Ending loop. ---")
                return "The agent could not complete the request because it failed to choose a valid action format."

        return "Agent reached maximum iterations without finishing."
