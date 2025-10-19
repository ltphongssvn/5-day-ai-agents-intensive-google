# common/base/agent.py - Base class for all agents

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.metrics: Dict[str, Any] = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
        }

    @abstractmethod
    def perceive(self, input_data: Any) -> Any:
        """Process input and return perception."""
        pass

    @abstractmethod
    def decide(self, perception: Any) -> Any:
        """Make decision based on perception."""
        pass

    @abstractmethod
    def act(self, decision: Any) -> Any:
        """Execute action based on decision."""
        pass

    def run(self, input_data: Any) -> Any:
        """Main execution loop: perceive -> decide -> act."""
        try:
            self.metrics["total_requests"] += 1
            perception = self.perceive(input_data)
            decision = self.decide(perception)
            result = self.act(decision)
            self.metrics["successful_requests"] += 1
            return result
        except Exception as e:
            self.metrics["failed_requests"] += 1
            raise e

    def get_metrics(self) -> Dict[str, Any]:
        """Return agent performance metrics."""
        return self.metrics.copy()