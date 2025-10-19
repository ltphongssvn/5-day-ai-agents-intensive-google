# day5/orchestrator/agent.py - Orchestrator for coordinating multiple agents

from typing import Any, Dict, List, Optional
from common.base.agent import BaseAgent


class OrchestratorAgent(BaseAgent):
    """Coordinates multiple specialized agents."""

    def __init__(self):
        super().__init__(
            name="OrchestratorAgent",
            description="Coordinates and routes tasks to specialized agents"
        )
        self.registered_agents: Dict[str, BaseAgent] = {}
        self.task_history: List[Dict[str, Any]] = []

    def register_agent(self, agent_type: str, agent: BaseAgent):
        """Register a specialized agent."""
        self.registered_agents[agent_type] = agent

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Analyze task requirements."""
        task = str(input_data).lower()

        return {
            "task": input_data,
            "task_lower": task,
            "requires_search": "search" in task or "find" in task,
            "requires_code": "code" in task or "execute" in task,
            "requires_memory": "remember" in task or "recall" in task,
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Route to appropriate agent(s)."""
        agents_needed = []

        if perception["requires_search"]:
            agents_needed.append("web_search")
        if perception["requires_code"]:
            agents_needed.append("code_execution")
        if perception["requires_memory"]:
            agents_needed.append("conversational")

        if not agents_needed:
            agents_needed.append("simple_reflex")

        return {
            "task": perception["task"],
            "agents": agents_needed,
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using selected agents."""
        results = []

        for agent_type in decision["agents"]:
            if agent_type in self.registered_agents:
                agent = self.registered_agents[agent_type]
                try:
                    result = agent.run(decision["task"])
                    results.append({
                        "agent": agent_type,
                        "result": result,
                        "success": True,
                    })
                except Exception as e:
                    results.append({
                        "agent": agent_type,
                        "error": str(e),
                        "success": False,
                    })

        # Record task
        self.task_history.append({
            "task": decision["task"],
            "agents_used": decision["agents"],
            "results_count": len(results),
        })

        return {
            "task": decision["task"],
            "agents_used": decision["agents"],
            "results": results,
        }

    def get_orchestration_stats(self) -> Dict[str, Any]:
        """Get orchestration statistics."""
        return {
            "registered_agents": list(self.registered_agents.keys()),
            "total_tasks": len(self.task_history),
            "metrics": self.get_metrics(),
        }


# Demo function
def demo():
    from day1.simple_reflex.agent import SimpleReflexAgent
    from day2.web_search.agent import WebSearchAgent
    from day2.code_execution.agent import CodeExecutionAgent

    orchestrator = OrchestratorAgent()

    # Register agents
    orchestrator.register_agent("simple_reflex", SimpleReflexAgent())
    orchestrator.register_agent("web_search", WebSearchAgent())
    orchestrator.register_agent("code_execution", CodeExecutionAgent())

    test_tasks = [
        "hello",
        "search for Python tutorials",
        "execute code: print('Hello')",
    ]

    print(f"=== {orchestrator.name} Demo ===\n")
    for task in test_tasks:
        result = orchestrator.run(task)
        print(f"Task: {result['task']}")
        print(f"Agents: {', '.join(result['agents_used'])}")
        for r in result['results']:
            if r['success']:
                print(f"  ✓ {r['agent']}: Success")
        print()

    stats = orchestrator.get_orchestration_stats()
    print(f"Stats: {stats['total_tasks']} tasks, {len(stats['registered_agents'])} agents")


if __name__ == "__main__":
    demo()