# day1/simple_reflex/agent.py - Simple reflex agent with rule-based responses

from typing import Any, Dict
from common.base.agent import BaseAgent


class SimpleReflexAgent(BaseAgent):
    """Agent that responds based on simple condition-action rules."""

    def __init__(self):
        super().__init__(
            name="SimpleReflexAgent",
            description="Rule-based agent with direct stimulus-response mapping"
        )
        self.rules: Dict[str, str] = {
            "hello": "Hello! How can I help you?",
            "help": "I can respond to: hello, help, weather, time, bye",
            "weather": "I don't have real-time weather data yet.",
            "time": "I don't have access to current time yet.",
            "bye": "Goodbye! Have a great day!",
        }

    def perceive(self, input_data: Any) -> str:
        """Convert input to lowercase string."""
        return str(input_data).lower().strip()

    def decide(self, perception: str) -> str:
        """Match perception to rules."""
        for keyword, response in self.rules.items():
            if keyword in perception:
                return response
        return "default"

    def act(self, decision: str) -> str:
        """Return response or default message."""
        if decision == "default":
            return "I don't understand. Type 'help' for available commands."
        return decision


# Demo function
def demo():
    agent = SimpleReflexAgent()

    test_inputs = ["hello", "help", "what's the weather?", "bye", "random text"]

    print(f"=== {agent.name} Demo ===\n")
    for input_text in test_inputs:
        response = agent.run(input_text)
        print(f"Input: {input_text}")
        print(f"Output: {response}\n")

    print(f"Metrics: {agent.get_metrics()}")


if __name__ == "__main__":
    demo()