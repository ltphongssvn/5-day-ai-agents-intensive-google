# day1/model_based/agent.py - Model-based agent with internal state tracking

from typing import Any, Dict, List
from datetime import datetime
from common.base.agent import BaseAgent


class ModelBasedAgent(BaseAgent):
    """Agent that maintains internal state and world model."""

    def __init__(self):
        super().__init__(
            name="ModelBasedAgent",
            description="Agent with internal state and world model"
        )
        # World model - internal representation
        self.world_state: Dict[str, Any] = {
            "conversation_history": [],
            "user_preferences": {},
            "context": {},
            "last_interaction": None,
        }

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Process input and update world model."""
        perception = {
            "input": str(input_data),
            "timestamp": datetime.now(),
            "input_length": len(str(input_data)),
        }

        # Update world state
        self.world_state["conversation_history"].append(perception)
        self.world_state["last_interaction"] = perception["timestamp"]

        return perception

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Make decision based on current state and history."""
        input_text = perception["input"].lower()
        history_count = len(self.world_state["conversation_history"])

        # Decision based on state
        decision = {
            "response_type": "acknowledgment",
            "include_history": history_count > 1,
            "personalize": False,
        }

        # Check for questions about history
        if "how many" in input_text or "count" in input_text:
            decision["response_type"] = "history_count"
        elif "first" in input_text:
            decision["response_type"] = "first_message"
        elif "previous" in input_text or "last" in input_text:
            decision["response_type"] = "previous_message"

        return decision

    def act(self, decision: Dict[str, Any]) -> str:
        """Generate response based on decision and state."""
        response_type = decision["response_type"]

        if response_type == "history_count":
            count = len(self.world_state["conversation_history"])
            return f"We've had {count} interaction(s) so far."

        elif response_type == "first_message":
            if self.world_state["conversation_history"]:
                first = self.world_state["conversation_history"][0]
                return f"Your first message was: '{first['input']}'"
            return "This is our first interaction."

        elif response_type == "previous_message":
            if len(self.world_state["conversation_history"]) > 1:
                prev = self.world_state["conversation_history"][-2]
                return f"Your previous message was: '{prev['input']}'"
            return "No previous message found."

        else:
            count = len(self.world_state["conversation_history"])
            return f"Message received. Total interactions: {count}"

    def get_state(self) -> Dict[str, Any]:
        """Return current world state."""
        return {
            "total_interactions": len(self.world_state["conversation_history"]),
            "last_interaction": self.world_state["last_interaction"],
            "context_size": len(self.world_state["context"]),
        }


# Demo function
def demo():
    agent = ModelBasedAgent()

    test_inputs = [
        "Hello there!",
        "What's the weather?",
        "How many messages have we exchanged?",
        "What was my first message?",
        "What was my previous message?",
    ]

    print(f"=== {agent.name} Demo ===\n")
    for input_text in test_inputs:
        response = agent.run(input_text)
        print(f"Input: {input_text}")
        print(f"Output: {response}")
        print(f"State: {agent.get_state()}\n")

    print(f"Metrics: {agent.get_metrics()}")


if __name__ == "__main__":
    demo()