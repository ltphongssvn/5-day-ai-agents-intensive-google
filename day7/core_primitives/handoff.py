# day7/core_primitives/handoff.py - Handoff primitive for agent delegation

from typing import Any, Dict, Optional, Callable
from datetime import datetime
from enum import Enum
from common.base.agent import BaseAgent


class HandoffStatus(Enum):
    """Status of handoff operation."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Handoff:
    """
    Handoff Primitive: Control Delegation to other Agents
    Enables agents to delegate tasks to other specialized agents.
    """

    def __init__(
        self,
        from_agent: str,
        to_agent: str,
        context: Dict[str, Any],
        condition: Optional[Callable[[Any], bool]] = None,
    ):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.context = context
        self.condition = condition
        self.status = HandoffStatus.PENDING
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.result: Optional[Any] = None
        self.error: Optional[str] = None

    def should_handoff(self, input_data: Any) -> bool:
        """Check if handoff condition is met."""
        if self.condition is None:
            return True
        return self.condition(input_data)

    def execute(self, target_agent: BaseAgent, input_data: Any) -> Any:
        """Execute the handoff to target agent."""
        try:
            self.status = HandoffStatus.IN_PROGRESS

            # Add handoff context to input
            handoff_input = {
                "original_input": input_data,
                "context": self.context,
                "from_agent": self.from_agent,
            }

            # Execute on target agent
            self.result = target_agent.run(handoff_input)

            self.status = HandoffStatus.COMPLETED
            self.completed_at = datetime.now()

            return self.result

        except Exception as e:
            self.status = HandoffStatus.FAILED
            self.error = str(e)
            self.completed_at = datetime.now()
            raise e

    def get_info(self) -> Dict[str, Any]:
        """Get handoff information."""
        return {
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "has_result": self.result is not None,
            "error": self.error,
        }


class HandoffManager:
    """
    Manages handoffs between multiple agents.
    Tracks handoff chain and enables complex delegation patterns.
    """

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.handoffs: list[Handoff] = []
        self.handoff_chain: list[str] = []

    def register_agent(self, name: str, agent: BaseAgent):
        """Register an agent for handoff."""
        self.agents[name] = agent

    def create_handoff(
        self,
        from_agent: str,
        to_agent: str,
        context: Dict[str, Any],
        condition: Optional[Callable[[Any], bool]] = None,
    ) -> Handoff:
        """Create a handoff between agents."""
        if to_agent not in self.agents:
            raise ValueError(f"Target agent '{to_agent}' not registered")

        handoff = Handoff(from_agent, to_agent, context, condition)
        self.handoffs.append(handoff)
        return handoff

    def execute_handoff(self, handoff: Handoff, input_data: Any) -> Any:
        """Execute a handoff."""
        if not handoff.should_handoff(input_data):
            return None

        target_agent = self.agents[handoff.to_agent]
        self.handoff_chain.append(f"{handoff.from_agent} -> {handoff.to_agent}")

        result = handoff.execute(target_agent, input_data)
        return result

    def handoff_to(
        self,
        from_agent: str,
        to_agent: str,
        input_data: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Quick handoff method."""
        handoff = self.create_handoff(
            from_agent,
            to_agent,
            context or {},
        )
        return self.execute_handoff(handoff, input_data)

    def get_handoff_chain(self) -> list[str]:
        """Get the handoff chain."""
        return self.handoff_chain.copy()

    def get_metrics(self) -> Dict[str, Any]:
        """Get handoff metrics."""
        total = len(self.handoffs)
        completed = sum(1 for h in self.handoffs if h.status == HandoffStatus.COMPLETED)
        failed = sum(1 for h in self.handoffs if h.status == HandoffStatus.FAILED)

        return {
            "total_handoffs": total,
            "completed": completed,
            "failed": failed,
            "success_rate": completed / total if total > 0 else 0,
            "handoff_chain_length": len(self.handoff_chain),
        }


# Demo function
def demo():
    """Demonstrate handoff mechanism."""
    from day1.simple_reflex.agent import SimpleReflexAgent

    print("=== Handoff Primitive Demo ===\n")

    # Create agents
    agent1 = SimpleReflexAgent()
    agent1.name = "GreeterAgent"

    agent2 = SimpleReflexAgent()
    agent2.name = "HelpAgent"

    # Create handoff manager
    manager = HandoffManager()
    manager.register_agent("greeter", agent1)
    manager.register_agent("helper", agent2)

    # Demo 1: Simple handoff
    print("--- Simple Handoff ---")
    handoff = manager.create_handoff(
        from_agent="greeter",
        to_agent="helper",
        context={"reason": "User needs help"},
    )

    result = manager.execute_handoff(handoff, "help")
    print(f"Handoff result: {result}")
    print(f"Handoff info: {handoff.get_info()}\n")

    # Demo 2: Conditional handoff
    print("--- Conditional Handoff ---")

    def needs_help(input_data):
        return "help" in str(input_data).lower()

    handoff2 = manager.create_handoff(
        from_agent="greeter",
        to_agent="helper",
        context={"reason": "Help keyword detected"},
        condition=needs_help,
    )

    print("Testing with 'hello':")
    if handoff2.should_handoff("hello"):
        result = manager.execute_handoff(handoff2, "hello")
        print(f"  Handoff executed: {result}")
    else:
        print("  Handoff skipped (condition not met)")

    print("\nTesting with 'I need help':")
    handoff3 = manager.create_handoff(
        from_agent="greeter",
        to_agent="helper",
        context={"reason": "Help keyword detected"},
        condition=needs_help,
    )
    if handoff3.should_handoff("I need help"):
        result = manager.execute_handoff(handoff3, "I need help")
        print(f"  Handoff executed: {result}")

    # Show metrics
    print("\n--- Handoff Metrics ---")
    print(f"Handoff chain: {manager.get_handoff_chain()}")
    print(f"Metrics: {manager.get_metrics()}")


if __name__ == "__main__":
    demo()
