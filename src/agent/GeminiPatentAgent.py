# src/agent.py
import json
import re
from . import tools
from . import prompts
from .memory import AgentMemory

class GeminiPatentAgent:
    """The core agent for handling patent analysis."""

    def __init__(self, model):
        """
        Initializes the agent.
        Args:
            model: An instance of a generative AI model (like Google's Gemini).
        """
        self.model = model
        self.memory = AgentMemory()
        self.available_tools = {
            "patent_search": tools.patent_search,
            "final_report": tools.final_report
        }
        print("--- Gemini Patent Agent Initialized ---")

    def _call_gemini(self, prompt):
        """A wrapper for calling the generative model."""
        # In a real application, add error handling, etc.
        response = self.model.generate_content(prompt)
        return response.text

    def _parse_action(self, llm_output: str):
        """Uses regex to parse the LLM's output for an action."""
        match = re.search(r"Action:\s*(\w+)\((.*)\)", llm_output)
        if match:
            tool_name = match.group(1).strip()
            tool_input_str = match.group(2).strip()
            # A simple way to handle string inputs for now
            tool_input = tool_input_str.strip("'\"")
            return tool_name, tool_input
        return None, None

    def run(self, user_input: str, max_iterations=5):
        """
        Runs the agent's core ReAct (Reason + Act) loop.
        """
        print(f"\n--- Running Agent with Input ---")
        
        # 1. Start with the initial planning prompt
        planning_prompt = prompts.REACT_PLANNING_PROMPT.format(user_input=user_input)
        self.memory.add_entry(f"User Input: {user_input}")

        # This will hold the results from our tool calls
        observation_results = {}
        
        for i in range(max_iterations):
            print(f"\n--- Iteration {i+1} ---")
            
            # 2. REASON: The AI "thinks" about what to do next.
            current_prompt = f"{planning_prompt}\n{self.memory.get_history()}"
            llm_response = self._call_gemini(current_prompt)
            self.memory.add_entry(f"LLM Response:\n{llm_response}")
            print(llm_response) # Log the agent's thoughts

            # 3. ACT: Parse the action and call the appropriate tool.
            tool_name, tool_input = self._parse_action(llm_response)

            if tool_name in self.available_tools:
                # If the agent wants to use a tool...
                tool_function = self.available_tools[tool_name]
                result = tool_function(tool_input)
                
                # Store the result of the tool action
                observation_results[tool_name] = result
                
                # Add the observation to memory for the next loop
                observation_entry = f"Observation: Tool `{tool_name}` returned: {json.dumps(result, indent=2)}"
                self.memory.add_entry(observation_entry)
                print(observation_entry)

                if tool_name == "final_report":
                    # 4. GENERATE FINAL RESPONSE: The final step has been triggered.
                    print("\n--- Generating Final Report ---")
                    final_prompt = prompts.FINAL_REPORT_PROMPT.format(
                        invention_text=user_input,
                        search_results=json.dumps(observation_results.get("patent_search"), indent=2)
                    )
                    final_analysis = self._call_gemini(final_prompt)
                    return final_analysis

            elif "final report" in llm_response.lower():
                # Failsafe in case the regex fails but the agent wants to finish
                print("\n--- Failsafe: Generating Final Report ---")
                final_prompt = prompts.FINAL_REPORT_PROMPT.format(
                    invention_text=user_input,
                    search_results=json.dumps(observation_results.get("patent_search"), indent=2)
                )
                final_analysis = self._call_gemini(final_prompt)
                return final_analysis
            
            else:
                print("--- Agent did not choose a valid action. Ending loop. ---")
                return "The agent could not complete the request."

        return "Agent reached maximum iterations without finishing."
