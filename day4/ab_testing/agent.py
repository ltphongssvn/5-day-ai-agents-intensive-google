# day4/ab_testing/agent.py - A/B testing agent for strategy comparison

from typing import Any, Dict, List, Callable
import random
from common.base.agent import BaseAgent


class ABTestingAgent(BaseAgent):
    """Agent that tests multiple strategies and compares performance."""

    def __init__(self):
        super().__init__(
            name="ABTestingAgent",
            description="Agent with A/B testing capabilities"
        )
        self.strategies = {
            "strategy_a": self._strategy_a,
            "strategy_b": self._strategy_b,
        }
        self.experiment_results = {
            "strategy_a": {"successes": 0, "total": 0, "scores": []},
            "strategy_b": {"successes": 0, "total": 0, "scores": []},
        }
        self.current_strategy = None

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Parse input."""
        return {
            "input": str(input_data),
            "length": len(str(input_data)),
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Randomly assign strategy for testing."""
        strategy_name = random.choice(list(self.strategies.keys()))
        self.current_strategy = strategy_name

        return {
            "strategy": strategy_name,
            "input": perception["input"],
        }

    def act(self, decision: Dict[str, Any]) -> str:
        """Execute selected strategy."""
        strategy_func = self.strategies[decision["strategy"]]
        result = strategy_func(decision["input"])

        # Record result
        self._record_experiment(decision["strategy"], result)

        return result["response"]

    def _strategy_a(self, input_text: str) -> Dict[str, Any]:
        """Strategy A: Simple response."""
        return {
            "response": f"A: {input_text.upper()}",
            "score": 0.7,
            "success": True,
        }

    def _strategy_b(self, input_text: str) -> Dict[str, Any]:
        """Strategy B: Enhanced response."""
        return {
            "response": f"B: Enhanced processing of '{input_text}'",
            "score": 0.85,
            "success": True,
        }

    def _record_experiment(self, strategy: str, result: Dict[str, Any]):
        """Record experiment results."""
        self.experiment_results[strategy]["total"] += 1
        if result["success"]:
            self.experiment_results[strategy]["successes"] += 1
        self.experiment_results[strategy]["scores"].append(result["score"])

    def get_experiment_results(self) -> Dict[str, Any]:
        """Analyze and compare strategies."""
        results = {}
        for strategy, data in self.experiment_results.items():
            if data["total"] > 0:
                results[strategy] = {
                    "total_runs": data["total"],
                    "success_rate": data["successes"] / data["total"],
                    "avg_score": sum(data["scores"]) / len(data["scores"]),
                }

        # Determine winner
        if results:
            winner = max(results.items(), key=lambda x: x[1]["avg_score"])
            results["winner"] = winner[0]

        return results


# Demo function
def demo():
    agent = ABTestingAgent()

    test_inputs = ["test1", "test2", "test3", "test4", "test5", "test6", "test7", "test8"]

    print(f"=== {agent.name} Demo ===\n")
    print("Running experiments...\n")

    for inp in test_inputs:
        response = agent.run(inp)
        print(f"Input: {inp} -> {response}")

    print("\n" + "="*50)
    print("Experiment Results:\n")

    results = agent.get_experiment_results()
    for strategy, metrics in results.items():
        if strategy != "winner":
            print(f"{strategy}:")
            print(f"  Runs: {metrics['total_runs']}")
            print(f"  Success rate: {metrics['success_rate']:.1%}")
            print(f"  Avg score: {metrics['avg_score']:.2f}\n")

    print(f"Winner: {results.get('winner', 'N/A')}")
    print(f"\nAgent Metrics: {agent.get_metrics()}")


if __name__ == "__main__":
    demo()