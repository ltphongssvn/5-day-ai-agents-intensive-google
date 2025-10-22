# day7/tool_types/agents_as_tools.py - Agents as Tools for hierarchical subtasking

from typing import Any, Dict, List
from datetime import datetime
from common.base.agent import BaseAgent


class AgentTool:
    """
    Wraps an agent as a tool that can be called by other agents.
    Enables hierarchical subtasking.
    """

    def __init__(
        self,
        agent: BaseAgent,
        description: str,
        parameters_schema: Dict[str, Any],
    ):
        self.agent = agent
        self.description = description
        self.parameters_schema = parameters_schema
        self.call_history: List[Dict[str, Any]] = []

    def execute(self, **kwargs) -> Any:
        """Execute the wrapped agent."""
        start_time = datetime.now()

        try:
            # Extract input from kwargs
            input_data = kwargs.get("input", kwargs)

            # Run the agent
            result = self.agent.run(input_data)

            # Log execution
            self.call_history.append(
                {
                    "timestamp": start_time.isoformat(),
                    "input": input_data,
                    "result": result,
                    "success": True,
                    "duration_ms": (datetime.now() - start_time).total_seconds() * 1000,
                }
            )

            return result

        except Exception as e:
            self.call_history.append(
                {
                    "timestamp": start_time.isoformat(),
                    "input": kwargs,
                    "error": str(e),
                    "success": False,
                }
            )
            raise e

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI tool schema."""
        return {
            "type": "function",
            "function": {
                "name": self.agent.name.lower().replace(" ", "_"),
                "description": self.description,
                "parameters": self.parameters_schema,
            },
        }

    def get_call_history(self) -> List[Dict[str, Any]]:
        """Get call history."""
        return self.call_history.copy()


class HierarchicalTaskManager:
    """
    Manages hierarchical task delegation using agents as tools.
    """

    def __init__(self, coordinator_agent: BaseAgent):
        self.coordinator = coordinator_agent
        self.sub_agents: Dict[str, AgentTool] = {}
        self.task_tree: List[Dict[str, Any]] = []

    def register_sub_agent(
        self,
        agent: BaseAgent,
        description: str,
        parameters_schema: Dict[str, Any],
    ):
        """Register a sub-agent as a tool."""
        agent_tool = AgentTool(agent, description, parameters_schema)
        self.sub_agents[agent.name] = agent_tool

    def delegate_task(self, task: str, sub_agent_name: str, **kwargs) -> Any:
        """Delegate a task to a sub-agent."""
        if sub_agent_name not in self.sub_agents:
            raise ValueError(f"Sub-agent '{sub_agent_name}' not registered")

        agent_tool = self.sub_agents[sub_agent_name]

        # Record in task tree
        task_record = {
            "task": task,
            "delegated_to": sub_agent_name,
            "timestamp": datetime.now().isoformat(),
        }
        self.task_tree.append(task_record)

        # Execute
        result = agent_tool.execute(input=task, **kwargs)
        task_record["result"] = result
        task_record["completed"] = True

        return result

    def execute_hierarchical_task(
        self,
        main_task: str,
        subtasks: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Execute a hierarchical task by delegating subtasks.

        Args:
            main_task: The main task description
            subtasks: List of {"task": str, "agent": str} dicts
        """
        results = {
            "main_task": main_task,
            "subtask_results": [],
        }

        for subtask in subtasks:
            result = self.delegate_task(
                subtask["task"],
                subtask["agent"],
            )
            results["subtask_results"].append(
                {
                    "task": subtask["task"],
                    "agent": subtask["agent"],
                    "result": result,
                }
            )

        return results

    def get_task_tree(self) -> List[Dict[str, Any]]:
        """Get the task delegation tree."""
        return self.task_tree.copy()

    def get_metrics(self) -> Dict[str, Any]:
        """Get hierarchical task metrics."""
        return {
            "coordinator": self.coordinator.name,
            "sub_agents": len(self.sub_agents),
            "total_delegations": len(self.task_tree),
            "sub_agent_names": list(self.sub_agents.keys()),
        }


# Demo function
def demo():
    """Demonstrate agents as tools."""
    from day1.simple_reflex.agent import SimpleReflexAgent

    print("=== Agents as Tools Demo ===\n")

    # Create coordinator
    coordinator = SimpleReflexAgent()
    coordinator.name = "CoordinatorAgent"

    # Create sub-agents
    greeter = SimpleReflexAgent()
    greeter.name = "GreeterAgent"

    helper = SimpleReflexAgent()
    helper.name = "HelperAgent"

    # Create hierarchical manager
    manager = HierarchicalTaskManager(coordinator)

    # Register sub-agents
    manager.register_sub_agent(
        greeter,
        "Handles greeting and welcome messages",
        {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "User input"},
            },
            "required": ["input"],
        },
    )

    manager.register_sub_agent(
        helper,
        "Provides help and assistance",
        {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "User input"},
            },
            "required": ["input"],
        },
    )

    # Demo 1: Simple delegation
    print("--- Simple Delegation ---")
    result = manager.delegate_task("hello", "GreeterAgent")
    print("Task: hello")
    print("Delegated to: GreeterAgent")
    print(f"Result: {result}\n")

    # Demo 2: Hierarchical task
    print("--- Hierarchical Task Execution ---")
    results = manager.execute_hierarchical_task(
        "Onboard new user",
        [
            {"task": "hello", "agent": "GreeterAgent"},
            {"task": "help", "agent": "HelperAgent"},
        ],
    )

    print(f"Main task: {results['main_task']}")
    for i, subtask_result in enumerate(results["subtask_results"], 1):
        print(f"  Subtask {i}: {subtask_result['task']}")
        print(f"    Agent: {subtask_result['agent']}")
        print(f"    Result: {subtask_result['result']}")

    # Show task tree
    print("\n--- Task Tree ---")
    for i, task in enumerate(manager.get_task_tree(), 1):
        print(f"{i}. {task['task']} -> {task['delegated_to']}")

    # Show metrics
    print("\n--- Metrics ---")
    metrics = manager.get_metrics()
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # Show OpenAI schemas
    print("\n--- OpenAI Tool Schemas ---")
    for name, agent_tool in manager.sub_agents.items():
        schema = agent_tool.to_openai_schema()
        print(f"{name}: {schema['function']['name']}")


if __name__ == "__main__":
    demo()
