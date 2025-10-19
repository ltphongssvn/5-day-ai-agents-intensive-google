# day4/self_monitoring/agent.py - Self-monitoring agent with observability

from typing import Any, Dict, List
from datetime import datetime
import time
from common.base.agent import BaseAgent


class SelfMonitoringAgent(BaseAgent):
    """Agent with detailed logging and performance tracking."""

    def __init__(self):
        super().__init__(
            name="SelfMonitoringAgent",
            description="Agent with self-evaluation and observability"
        )
        self.detailed_metrics = {
            "response_times": [],
            "error_log": [],
            "performance_scores": [],
        }

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Perceive with timing."""
        start_time = time.time()

        perception = {
            "input": str(input_data),
            "length": len(str(input_data)),
            "timestamp": datetime.now(),
        }

        perception["perceive_time"] = time.time() - start_time
        return perception

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Decide with performance tracking."""
        start_time = time.time()

        decision = {
            "action": "process",
            "confidence": 0.85,
        }

        decision["decide_time"] = time.time() - start_time
        return decision

    def act(self, decision: Dict[str, Any]) -> str:
        """Act with result evaluation."""
        start_time = time.time()

        response = f"Processed with {decision['confidence']:.0%} confidence"

        act_time = time.time() - start_time

        # Self-evaluate
        self._evaluate_performance(decision, act_time)

        return response

    def _evaluate_performance(self, decision: Dict[str, Any], act_time: float):
        """Evaluate and log performance."""
        total_time = decision.get("perceive_time", 0) + decision.get("decide_time", 0) + act_time

        self.detailed_metrics["response_times"].append(total_time)

        # Performance score based on speed and confidence
        score = decision["confidence"] * (1.0 if total_time < 0.1 else 0.8)
        self.detailed_metrics["performance_scores"].append(score)

    def get_detailed_metrics(self) -> Dict[str, Any]:
        """Return comprehensive metrics."""
        response_times = self.detailed_metrics["response_times"]
        scores = self.detailed_metrics["performance_scores"]

        return {
            **self.get_metrics(),
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "max_response_time": max(response_times) if response_times else 0,
            "avg_performance_score": sum(scores) / len(scores) if scores else 0,
            "total_errors": len(self.detailed_metrics["error_log"]),
        }


# Demo function
def demo():
    agent = SelfMonitoringAgent()

    test_inputs = [
        "Hello",
        "Process this data",
        "Another request",
        "Final test",
    ]

    print(f"=== {agent.name} Demo ===\n")
    for inp in test_inputs:
        response = agent.run(inp)
        print(f"Input: {inp}")
        print(f"Output: {response}\n")

    metrics = agent.get_detailed_metrics()
    print("Performance Metrics:")
    print(f"  Total requests: {metrics['total_requests']}")
    print(f"  Success rate: {metrics['successful_requests']/metrics['total_requests']:.1%}")
    print(f"  Avg response time: {metrics['avg_response_time']*1000:.2f}ms")
    print(f"  Avg performance score: {metrics['avg_performance_score']:.2f}")


if __name__ == "__main__":
    demo()