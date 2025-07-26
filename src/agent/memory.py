# src/memory.py

class AgentMemory:
    """
    A simple class to store the agent's conversation history.
    Used by the agent to maintain context across multiple reasoning and tool-calling steps.
    """
    def __init__(self):
        # This list will hold all conversation entries in order (user input, LLM thoughts, tool calls, etc.)
        self._history = []

    def add_entry(self, entry: str):
        """
        Adds a new thought, action, or observation to the memory.
        Args:
            entry (str): The string to add to the conversation history.
        """
        # Append the new entry (could be user input, LLM response, or tool result) to the end of the history list
        self._history.append(entry)

    def get_history(self) -> str:
        """
        Returns the entire history as a formatted string.
        This is used to provide full context to the LLM at each step.
        Returns:
            str: The conversation history, with each entry separated by a newline.
        """
        # Join all entries in the history list with newline characters to form a single string
        # This string is then used as context for the next LLM prompt
        return "\n".join(self._history)