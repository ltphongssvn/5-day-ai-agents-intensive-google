# day3/conversational/agent.py - Conversational agent with session memory

from typing import Any, Dict, List, Optional
from datetime import datetime
from common.base.agent import BaseAgent


class ConversationalAgent(BaseAgent):
    """Agent with short-term memory for multi-turn conversations."""

    def __init__(self, max_history: int = 10):
        super().__init__(
            name="ConversationalAgent",
            description="Agent with session memory and context tracking"
        )
        self.max_history = max_history
        self.conversation_memory: List[Dict[str, Any]] = []
        self.context_window: List[str] = []

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Process input with conversation context."""
        user_input = str(input_data).strip()

        perception = {
            "input": user_input,
            "timestamp": datetime.now(),
            "turn_number": len(self.conversation_memory) + 1,
            "context_size": len(self.context_window),
        }

        return perception

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Decide response strategy based on context."""
        user_input = perception["input"].lower()

        # Analyze for context references
        has_pronoun = any(p in user_input for p in ['it', 'that', 'this', 'they'])
        asks_about_previous = any(w in user_input for w in ['before', 'earlier', 'previous'])

        decision = {
            "input": perception["input"],
            "use_context": has_pronoun or asks_about_previous,
            "summarize_context": perception["turn_number"] > 5,
        }

        return decision

    def act(self, decision: Dict[str, Any]) -> str:
        """Generate contextual response."""
        user_input = decision["input"]

        # Build response
        if decision["use_context"] and self.context_window:
            context = " ".join(self.context_window[-3:])
            response = f"Based on our conversation about {context}: I understand '{user_input}'"
        else:
            response = f"Message received: {user_input}"

        # Update memory
        self.conversation_memory.append({
            "user": user_input,
            "assistant": response,
            "timestamp": datetime.now(),
        })

        # Update context window
        self.context_window.append(user_input)
        if len(self.context_window) > self.max_history:
            self.context_window.pop(0)

        return response

    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation statistics."""
        return {
            "total_turns": len(self.conversation_memory),
            "context_window_size": len(self.context_window),
            "first_message": self.conversation_memory[0] if self.conversation_memory else None,
            "last_message": self.conversation_memory[-1] if self.conversation_memory else None,
        }


# Demo function
def demo():
    agent = ConversationalAgent(max_history=5)

    conversation = [
        "Hello, I'm interested in learning Python",
        "What topics should I start with?",
        "Can you tell me more about it?",
        "What did I say earlier?",
        "Thank you for the help",
    ]

    print(f"=== {agent.name} Demo ===\n")
    for user_msg in conversation:
        response = agent.run(user_msg)
        print(f"User: {user_msg}")
        print(f"Agent: {response}\n")

    summary = agent.get_conversation_summary()
    print(f"Conversation Summary:")
    print(f"  Total turns: {summary['total_turns']}")
    print(f"  Context size: {summary['context_window_size']}")
    print(f"\nMetrics: {agent.get_metrics()}")


if __name__ == "__main__":
    demo()