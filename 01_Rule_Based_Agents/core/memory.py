# This adds a memory module to the rule-based agent that keeps track of the conversation history.
from datetime import datetime
from typing import List, Dict

class ConversationMemory:
    def __init__(self, max_history=5):
        self.history: List[Dict] = []
        self.max_history = max_history
        self.context_stack = []

    def add_interaction(self, user_input: str, response: str):
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": response
        })
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_recent_context(self, lookback=2) -> str:
        return "\n".join(
            f"User: {entry['user']}\nAgent: {entry['agent']}" 
            for entry in self.history[-lookback:]
        )