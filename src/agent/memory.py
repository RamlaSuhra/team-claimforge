# src/memory.py

class AgentMemory:
    """A simple class to store the agent's conversation history."""
    def __init__(self):
        self._history = []

    def add_entry(self, entry: str):
        """Adds a new thought, action, or observation to the memory."""
        self._history.append(entry)

    def get_history(self) -> str:
        """Returns the entire history as a formatted string."""
        return "\n".join(self._history)