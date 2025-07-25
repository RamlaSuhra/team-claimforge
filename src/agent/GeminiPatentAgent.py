# src/agent.py
import json
import re
from . import tools
from . import prompts
from .memory import AgentMemory

class GeminiPatentAgent:
    """The core agent for handling patent analysis."""

    def __init__(self, model):
        self.model = model
        self.memory = AgentMemory()
        # The agent now knows about the tools available.
        self.available_tools = {
            "patent_search": tools.patent_search,
            "final_report": tools.final_report # The placeholder is now a real tool
        }
        print("--- Gemini Patent Agent Initialized ---")

    def _call_gemini(self, prompt):
        """A wrapper for calling the generative model for reasoning steps."""
        response = self.model.generate_content(prompt)
        return response.text

    def _parse_action(self, llm_output: str):
        """Uses regex to parse the LLM's output for an action."""
        # This regex can now handle actions with or without parameters (for final_report)
        match = re.search(r"Action:\s*(\w+)\((.*)\)", llm_output)
        if match:
            tool_name = match.group(1).strip()
            tool_input_str = match.group(2).strip()
            # Handle string inputs for patent_search
            tool_input = tool_input_str.strip("'\"") if tool_input_str else None
            return tool_name, tool_input
        return None, None

    def run(self, user_input: str, max_iterations=5):
        """
        Runs the agent's core ReAct (Reason + Act) loop.
        """
        print(f"\n--- Running Agent with Input ---")
        
        planning_prompt = prompts.REACT_PLANNING_PROMPT.format(user_input=user_input)
        self.memory.add_entry(f"User Input: {user_input}")

        # This will hold the results from our tool calls
        observation_results = {}
        
        for i in range(max_iterations):
            print(f"\n--- Iteration {i+1} ---")
            
            # REASON: The AI "thinks" about what to do next.
            current_prompt = f"{planning_prompt}\n{self.memory.get_history()}"
            llm_response = self._call_gemini(current_prompt)
            self.memory.add_entry(f"LLM Response:\n{llm_response}")
            print(llm_response)

            # ACT: Parse the action and call the appropriate tool.
            tool_name, tool_input = self._parse_action(llm_response)

            if tool_name in self.available_tools:
                tool_function = self.available_tools[tool_name]
                
                if tool_name == "patent_search":
                    result = tool_function(tool_input)
                    observation_results[tool_name] = result # Store search results
                    observation_entry = f"Observation: Tool `{tool_name}` returned: {json.dumps(result, indent=2)}"
                    self.memory.add_entry(observation_entry)
                    print(observation_entry)
                
                elif tool_name == "final_report":
                    # --- CORE CHANGE IS HERE ---
                    # The agent now calls the implemented tool with full context.
                    final_analysis = tool_function(
                        model=self.model,
                        invention_text=user_input,
                        search_results=observation_results.get("patent_search", []) # Pass stored results
                    )
                    # The tool's output is the final answer.
                    return final_analysis

            else:
                print("--- Agent did not choose a valid action. Ending loop. ---")
                return "The agent could not complete the request."

        return "Agent reached maximum iterations without finishing."