# day7/control_logic/patterns.py - Control Logic Framework: Iterative Loop, ReAct, CoT, Planner-Executor

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum
from common.base.agent import BaseAgent


class ControlPattern(Enum):
    """Available control logic patterns."""

    OBSERVE_REASON_ACT = "observe_reason_act"  # Basic iterative loop
    REACT = "react"  # Reasoning + Acting pattern
    CHAIN_OF_THOUGHT = "cot"  # Chain of Thought
    PLANNER_EXECUTOR = "planner_executor"  # Planning then execution


class ObserveReasonActController:
    """
    Iterative Loop: Observe -> Reason -> Act
    Basic control pattern for agent execution.
    """

    def __init__(self, agent: BaseAgent):
        self.agent = agent
        self.execution_log: List[Dict[str, Any]] = []

    def execute(self, input_data: Any) -> Any:
        """Execute one iteration of observe-reason-act."""
        timestamp = datetime.now()

        # Observe (Perceive)
        observation = self.agent.perceive(input_data)

        # Reason (Decide)
        reasoning = self.agent.decide(observation)

        # Act
        action = self.agent.act(reasoning)

        # Log execution
        self.execution_log.append(
            {
                "timestamp": timestamp,
                "observation": observation,
                "reasoning": reasoning,
                "action": action,
            }
        )

        return action

    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get execution log."""
        return self.execution_log.copy()


class ReActController:
    """
    ReAct Pattern: Reasoning + Acting
    Interleaves reasoning steps with actions, allowing for dynamic planning.
    """

    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations
        self.execution_trace: List[Dict[str, Any]] = []

    def execute(
        self,
        initial_input: Any,
        reasoning_function: Callable[[Any], str],
        action_function: Callable[[str], Any],
        stop_condition: Optional[Callable[[Any], bool]] = None,
    ) -> Any:
        """
        Execute ReAct pattern.

        Args:
            initial_input: Starting input
            reasoning_function: Function that generates reasoning/thought
            action_function: Function that executes action based on reasoning
            stop_condition: Optional function to determine when to stop
        """
        current_state = initial_input

        for iteration in range(self.max_iterations):
            # Thought: Generate reasoning
            thought = reasoning_function(current_state)

            # Action: Execute based on reasoning
            action_result = action_function(thought)

            # Log trace
            self.execution_trace.append(
                {
                    "iteration": iteration + 1,
                    "thought": thought,
                    "action": action_result,
                    "timestamp": datetime.now(),
                }
            )

            # Check stop condition
            if stop_condition and stop_condition(action_result):
                return action_result

            # Update state for next iteration
            current_state = action_result

        return current_state

    def get_trace(self) -> List[Dict[str, Any]]:
        """Get execution trace showing reasoning and actions."""
        return self.execution_trace.copy()

    def format_trace(self) -> str:
        """Format trace as readable string."""
        output = []
        for step in self.execution_trace:
            output.append(f"Iteration {step['iteration']}:")
            output.append(f"  Thought: {step['thought']}")
            output.append(f"  Action: {step['action']}\n")
        return "\n".join(output)


class ChainOfThoughtController:
    """
    Chain of Thought (CoT) Pattern
    Breaks down complex reasoning into explicit sequential steps.
    """

    def __init__(self):
        self.reasoning_chain: List[str] = []

    def execute(
        self,
        problem: str,
        reasoning_steps: List[Callable[[str], str]],
    ) -> str:
        """
        Execute chain of thought reasoning.

        Args:
            problem: Initial problem/query
            reasoning_steps: List of functions that perform reasoning steps
        """
        self.reasoning_chain = []
        current_context = problem

        for i, step_function in enumerate(reasoning_steps):
            step_result = step_function(current_context)
            self.reasoning_chain.append(
                {
                    "step": i + 1,
                    "reasoning": step_result,
                    "timestamp": datetime.now(),
                }
            )
            current_context = step_result

        return current_context

    def get_reasoning_chain(self) -> List[Dict[str, Any]]:
        """Get the complete reasoning chain."""
        return self.reasoning_chain.copy()

    def format_chain(self) -> str:
        """Format reasoning chain as readable string."""
        output = ["Chain of Thought:"]
        for step in self.reasoning_chain:
            output.append(f"Step {step['step']}: {step['reasoning']}")
        return "\n".join(output)


class PlannerExecutorController:
    """
    Planner-Executor Pattern
    Separates planning phase from execution phase.
    """

    def __init__(self):
        self._plan: List[Dict[str, Any]] = []
        self.execution_results: List[Dict[str, Any]] = []

    def plan(
        self,
        goal: str,
        planner_function: Callable[[str], List[str]],
    ) -> List[str]:
        """
        Planning phase: Generate plan to achieve goal.

        Args:
            goal: The objective to achieve
            planner_function: Function that generates plan steps
        """
        plan_steps = planner_function(goal)

        self._plan = [
            {
                "step_number": i + 1,
                "action": step,
                "status": "pending",
            }
            for i, step in enumerate(plan_steps)
        ]

        return plan_steps

    def execute(
        self,
        executor_function: Callable[[str], Any],
    ) -> List[Any]:
        """
        Execution phase: Execute each step in the plan.

        Args:
            executor_function: Function that executes a plan step
        """
        self.execution_results = []

        for plan_step in self._plan:
            try:
                result = executor_function(plan_step["action"])

                plan_step["status"] = "completed"
                self.execution_results.append(
                    {
                        "step_number": plan_step["step_number"],
                        "action": plan_step["action"],
                        "result": result,
                        "success": True,
                        "timestamp": datetime.now(),
                    }
                )

            except Exception as e:
                plan_step["status"] = "failed"
                self.execution_results.append(
                    {
                        "step_number": plan_step["step_number"],
                        "action": plan_step["action"],
                        "error": str(e),
                        "success": False,
                        "timestamp": datetime.now(),
                    }
                )

        return self.execution_results

    def get_plan(self) -> List[Dict[str, Any]]:
        """Get the current plan."""
        return self._plan.copy()

    def get_results(self) -> List[Dict[str, Any]]:
        """Get execution results."""
        return self.execution_results.copy()

    def format_plan_and_results(self) -> str:
        """Format plan and results as readable string."""
        output = ["=== Plan ==="]
        for step in self._plan:
            output.append(f"{step['step_number']}. {step['action']} [{step['status']}]")

        output.append("\n=== Execution Results ===")
        for result in self.execution_results:
            status = "✓" if result["success"] else "✗"
            output.append(f"{status} Step {result['step_number']}: {result['action']}")
            if result["success"]:
                output.append(f"   Result: {result['result']}")
            else:
                output.append(f"   Error: {result['error']}")

        return "\n".join(output)


# Demo function
def demo():
    """Demonstrate control logic patterns."""
    print("=== Control Logic Patterns Demo ===\n")

    # Demo 1: Observe-Reason-Act
    print("--- Observe-Reason-Act Pattern ---")
    from day1.simple_reflex.agent import SimpleReflexAgent

    agent = SimpleReflexAgent()
    controller = ObserveReasonActController(agent)

    result = controller.execute("hello")
    print("Input: hello")
    print(f"Output: {result}\n")

    # Demo 2: ReAct Pattern
    print("--- ReAct Pattern ---")
    react = ReActController(max_iterations=3)

    def reasoning(state):
        return f"Thinking about: {state}"

    def action(thought):
        return f"Executed action based on: {thought}"

    result = react.execute(
        "Solve problem X", reasoning, action, stop_condition=lambda x: "Executed" in x
    )
    print(react.format_trace())

    # Demo 3: Chain of Thought
    print("--- Chain of Thought Pattern ---")
    cot = ChainOfThoughtController()

    steps = [
        lambda x: f"Understanding problem: {x}",
        lambda x: "Breaking down into sub-problems",
        lambda x: "Solving each sub-problem",
        lambda x: "Combining solutions",
    ]

    result = cot.execute("What is 25 * 4?", steps)
    print(cot.format_chain())
    print(f"Final result: {result}\n")

    # Demo 4: Planner-Executor
    print("--- Planner-Executor Pattern ---")
    planner_executor = PlannerExecutorController()

    def create_plan(goal):
        return [
            "Gather requirements",
            "Design solution",
            "Implement code",
            "Test implementation",
        ]

    def executor_func(action):
        return f"Completed: {action}"

    planner_executor.plan("Build web app", create_plan)
    planner_executor.execute(executor_func)

    print(planner_executor.format_plan_and_results())


if __name__ == "__main__":
    demo()
