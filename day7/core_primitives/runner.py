# day7/core_primitives/runner.py - OpenAI Agents SDK Core Primitive: Runner (Execution Engine)

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum
from common.base.agent import BaseAgent


class ExecutionMode(Enum):
    """Execution modes for the runner."""

    SINGLE = "single"  # Execute once
    LOOP = "loop"  # Execute in iterative loop
    PARALLEL = "parallel"  # Execute multiple agents in parallel


class Runner:
    """
    Core Primitive: Runner
    Execution engine that manages agent execution, supports loops,
    and handles control flow for single or multiple agents.
    """

    def __init__(
        self,
        mode: ExecutionMode = ExecutionMode.SINGLE,
        max_iterations: int = 10,
        stop_condition: Optional[Callable[[Any], bool]] = None,
    ):
        self.mode = mode
        self.max_iterations = max_iterations
        self.stop_condition = stop_condition
        self.execution_history: List[Dict[str, Any]] = []
        self.metrics = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_iterations": 0,
        }

    def run_single(self, agent: BaseAgent, input_data: Any) -> Any:
        """Execute agent once with given input."""
        start_time = datetime.now()

        try:
            result = agent.run(input_data)

            execution_record = {
                "mode": "single",
                "agent": agent.name,
                "input": input_data,
                "output": result,
                "timestamp": start_time,
                "success": True,
            }

            self.execution_history.append(execution_record)
            self.metrics["total_executions"] += 1
            self.metrics["successful_executions"] += 1

            return result

        except Exception as e:
            execution_record = {
                "mode": "single",
                "agent": agent.name,
                "input": input_data,
                "error": str(e),
                "timestamp": start_time,
                "success": False,
            }

            self.execution_history.append(execution_record)
            self.metrics["total_executions"] += 1
            self.metrics["failed_executions"] += 1

            raise e

    def run_loop(self, agent: BaseAgent, initial_input: Any) -> List[Any]:
        """
        Execute agent in iterative loop.
        Continues until max_iterations or stop_condition is met.
        """
        results = []
        current_input = initial_input

        for iteration in range(self.max_iterations):
            start_time = datetime.now()

            try:
                result = agent.run(current_input)

                execution_record = {
                    "mode": "loop",
                    "iteration": iteration + 1,
                    "agent": agent.name,
                    "input": current_input,
                    "output": result,
                    "timestamp": start_time,
                    "success": True,
                }

                self.execution_history.append(execution_record)
                self.metrics["total_executions"] += 1
                self.metrics["successful_executions"] += 1
                self.metrics["total_iterations"] += 1

                results.append(result)

                # Check stop condition
                if self.stop_condition and self.stop_condition(result):
                    break

                # Use output as next input (feedback loop)
                current_input = result

            except Exception as e:
                execution_record = {
                    "mode": "loop",
                    "iteration": iteration + 1,
                    "agent": agent.name,
                    "input": current_input,
                    "error": str(e),
                    "timestamp": start_time,
                    "success": False,
                }

                self.execution_history.append(execution_record)
                self.metrics["total_executions"] += 1
                self.metrics["failed_executions"] += 1

                break

        return results

    def run_parallel(self, agents: List[BaseAgent], input_data: Any) -> List[Any]:
        """
        Execute multiple agents with same input.
        Returns list of results from each agent.
        """
        results = []
        start_time = datetime.now()

        for agent in agents:
            try:
                result = agent.run(input_data)

                execution_record = {
                    "mode": "parallel",
                    "agent": agent.name,
                    "input": input_data,
                    "output": result,
                    "timestamp": start_time,
                    "success": True,
                }

                self.execution_history.append(execution_record)
                self.metrics["total_executions"] += 1
                self.metrics["successful_executions"] += 1

                results.append(result)

            except Exception as e:
                execution_record = {
                    "mode": "parallel",
                    "agent": agent.name,
                    "input": input_data,
                    "error": str(e),
                    "timestamp": start_time,
                    "success": False,
                }

                self.execution_history.append(execution_record)
                self.metrics["total_executions"] += 1
                self.metrics["failed_executions"] += 1

                results.append(None)

        return results

    def run(self, agent_or_agents: Any, input_data: Any) -> Any:
        """
        Main execution method. Routes to appropriate execution mode.
        """
        if self.mode == ExecutionMode.SINGLE:
            return self.run_single(agent_or_agents, input_data)
        elif self.mode == ExecutionMode.LOOP:
            return self.run_loop(agent_or_agents, input_data)
        elif self.mode == ExecutionMode.PARALLEL:
            return self.run_parallel(agent_or_agents, input_data)

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Return execution history."""
        return self.execution_history.copy()

    def get_metrics(self) -> Dict[str, Any]:
        """Return execution metrics."""
        return self.metrics.copy()


# Demo function
def demo():
    """Demonstrate Runner with different execution modes."""
    from day1.simple_reflex.agent import SimpleReflexAgent

    print("=== Runner Core Primitive Demo ===\n")

    # Demo 1: Single execution
    print("--- Single Execution Mode ---")
    runner_single = Runner(mode=ExecutionMode.SINGLE)
    agent = SimpleReflexAgent()

    result = runner_single.run(agent, "hello")
    print("Input: hello")
    print(f"Output: {result}\n")

    # Demo 2: Loop execution
    print("--- Loop Execution Mode ---")

    class CounterAgent(BaseAgent):
        def __init__(self):
            super().__init__("CounterAgent", "Counts iterations")
            self.count = 0

        def perceive(self, input_data: Any) -> int:
            return int(input_data) if isinstance(input_data, (int, str)) else 0

        def decide(self, perception: int) -> int:
            return perception + 1

        def act(self, decision: int) -> int:
            self.count = decision
            return decision

    # Stop when count reaches 5
    def stop_at_5(result):
        return result >= 5

    runner_loop = Runner(
        mode=ExecutionMode.LOOP, max_iterations=10, stop_condition=stop_at_5
    )

    counter_agent = CounterAgent()
    results = runner_loop.run(counter_agent, 0)
    print(f"Loop results: {results}")
    print(f"Stopped at: {results[-1]}\n")

    # Demo 3: Parallel execution
    print("--- Parallel Execution Mode ---")
    runner_parallel = Runner(mode=ExecutionMode.PARALLEL)

    agent1 = SimpleReflexAgent()
    agent2 = SimpleReflexAgent()
    agent2.name = "SimpleReflexAgent2"

    results = runner_parallel.run([agent1, agent2], "help")
    print("Input: help")
    print(f"Agent1 output: {results[0]}")
    print(f"Agent2 output: {results[1]}\n")

    # Print metrics
    print("=== Metrics ===")
    print(f"Single mode: {runner_single.get_metrics()}")
    print(f"Loop mode: {runner_loop.get_metrics()}")
    print(f"Parallel mode: {runner_parallel.get_metrics()}")


if __name__ == "__main__":
    demo()
