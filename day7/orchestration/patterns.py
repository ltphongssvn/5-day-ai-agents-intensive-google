# day7/orchestration/patterns.py - Orchestration Patterns: Centralized, Hierarchical, Decentralized, Swarm

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum
from common.base.agent import BaseAgent


class OrchestrationPattern(Enum):
    """Orchestration architecture patterns."""

    CENTRALIZED = "centralized"
    HIERARCHICAL = "hierarchical"
    DECENTRALIZED = "decentralized"
    SWARM = "swarm"


class AgentHandoff:
    """
    Agent Hand-off mechanism for delegating tasks between agents.
    """

    def __init__(self, from_agent: str, to_agent: str, context: Dict[str, Any]):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.context = context
        self.timestamp = datetime.now()


class CentralizedOrchestrator:
    """
    Centralized Pattern: Single coordinator manages all agents.
    All communication flows through the central orchestrator.
    """

    def __init__(self, name: str = "CentralOrchestrator"):
        self.name = name
        self.agents: Dict[str, BaseAgent] = {}
        self.routing_rules: Dict[str, Callable[[Any], str]] = {}
        self.execution_log: List[Dict[str, Any]] = []

    def register_agent(self, agent_name: str, agent: BaseAgent):
        """Register an agent with the orchestrator."""
        self.agents[agent_name] = agent

    def register_routing_rule(
        self, rule_name: str, rule_function: Callable[[Any], str]
    ):
        """Register a routing rule for task assignment."""
        self.routing_rules[rule_name] = rule_function

    def route_task(self, task: Any, rule_name: str = "default") -> str:
        """Determine which agent should handle the task."""
        if rule_name in self.routing_rules:
            return self.routing_rules[rule_name](task)

        # Default: use first agent
        return list(self.agents.keys())[0] if self.agents else None

    def execute(self, task: Any, rule_name: str = "default") -> Any:
        """Execute task by routing to appropriate agent."""
        agent_name = self.route_task(task, rule_name)

        if not agent_name or agent_name not in self.agents:
            raise ValueError(f"No agent available for task: {task}")

        agent = self.agents[agent_name]
        result = agent.run(task)

        self.execution_log.append(
            {
                "timestamp": datetime.now(),
                "task": task,
                "assigned_to": agent_name,
                "result": result,
            }
        )

        return result

    def get_metrics(self) -> Dict[str, Any]:
        """Get orchestration metrics."""
        return {
            "total_agents": len(self.agents),
            "total_executions": len(self.execution_log),
            "agents": list(self.agents.keys()),
        }


class HierarchicalOrchestrator:
    """
    Hierarchical Pattern: Tree structure with supervisor agents.
    Tasks flow down, results flow up.
    """

    def __init__(self, root_agent: BaseAgent):
        self.root_agent = root_agent
        self.hierarchy: Dict[str, List[BaseAgent]] = {}
        self.execution_trace: List[Dict[str, Any]] = []

    def add_subordinate(self, supervisor_name: str, subordinate: BaseAgent):
        """Add a subordinate agent under a supervisor."""
        if supervisor_name not in self.hierarchy:
            self.hierarchy[supervisor_name] = []
        self.hierarchy[supervisor_name].append(subordinate)

    def execute(self, task: Any, decompose_function: Optional[Callable] = None) -> Any:
        """
        Execute task hierarchically.
        Root agent decomposes, subordinates execute, root aggregates.
        """
        # Root level processing
        root_result = self.root_agent.run(task)

        self.execution_trace.append(
            {
                "level": "root",
                "agent": self.root_agent.name,
                "task": task,
                "result": root_result,
                "timestamp": datetime.now(),
            }
        )

        # If root has subordinates, delegate subtasks
        if self.root_agent.name in self.hierarchy:
            subordinate_results = []

            for subordinate in self.hierarchy[self.root_agent.name]:
                sub_result = subordinate.run(root_result)
                subordinate_results.append(sub_result)

                self.execution_trace.append(
                    {
                        "level": "subordinate",
                        "agent": subordinate.name,
                        "task": root_result,
                        "result": sub_result,
                        "timestamp": datetime.now(),
                    }
                )

            return {
                "root_result": root_result,
                "subordinate_results": subordinate_results,
            }

        return root_result

    def get_trace(self) -> List[Dict[str, Any]]:
        """Get execution trace."""
        return self.execution_trace.copy()


class DecentralizedOrchestrator:
    """
    Decentralized Pattern: Peer-to-peer agent communication.
    Agents communicate directly without central coordinator.
    """

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.connections: Dict[str, List[str]] = {}
        self.message_log: List[Dict[str, Any]] = []

    def register_agent(self, agent_name: str, agent: BaseAgent):
        """Register an agent."""
        self.agents[agent_name] = agent
        self.connections[agent_name] = []

    def connect_agents(self, agent1: str, agent2: str):
        """Create bidirectional connection between agents."""
        if agent1 not in self.connections:
            self.connections[agent1] = []
        if agent2 not in self.connections:
            self.connections[agent2] = []

        if agent2 not in self.connections[agent1]:
            self.connections[agent1].append(agent2)
        if agent1 not in self.connections[agent2]:
            self.connections[agent2].append(agent1)

    def send_message(self, from_agent: str, to_agent: str, message: Any) -> Any:
        """Send message from one agent to another."""
        if to_agent not in self.connections.get(from_agent, []):
            raise ValueError(f"No connection between {from_agent} and {to_agent}")

        if to_agent not in self.agents:
            raise ValueError(f"Agent {to_agent} not found")

        result = self.agents[to_agent].run(message)

        self.message_log.append(
            {
                "from": from_agent,
                "to": to_agent,
                "message": message,
                "result": result,
                "timestamp": datetime.now(),
            }
        )

        return result

    def broadcast(self, from_agent: str, message: Any) -> List[Any]:
        """Broadcast message to all connected agents."""
        results = []

        for connected_agent in self.connections.get(from_agent, []):
            result = self.send_message(from_agent, connected_agent, message)
            results.append(result)

        return results

    def get_network_metrics(self) -> Dict[str, Any]:
        """Get network metrics."""
        return {
            "total_agents": len(self.agents),
            "total_connections": sum(len(conns) for conns in self.connections.values())
            // 2,
            "total_messages": len(self.message_log),
            "network_topology": self.connections,
        }


class SwarmOrchestrator:
    """
    Swarm Pattern: Emergent behavior from simple rules.
    Agents follow local rules, global behavior emerges.
    """

    def __init__(self, name: str = "SwarmOrchestrator"):
        self.name = name
        self.agents: List[BaseAgent] = []
        self.shared_state: Dict[str, Any] = {}
        self.execution_rounds: List[Dict[str, Any]] = []

    def add_agent(self, agent: BaseAgent):
        """Add agent to swarm."""
        self.agents.append(agent)

    def update_shared_state(self, key: str, value: Any):
        """Update shared state accessible to all agents."""
        self.shared_state[key] = value

    def execute_round(self, input_data: Any) -> List[Any]:
        """Execute one round where all agents process input."""
        round_results = []

        for agent in self.agents:
            # Each agent sees shared state and produces output
            result = agent.run(
                {
                    "input": input_data,
                    "shared_state": self.shared_state,
                }
            )
            round_results.append(result)

        self.execution_rounds.append(
            {
                "round": len(self.execution_rounds) + 1,
                "results": round_results,
                "shared_state": self.shared_state.copy(),
                "timestamp": datetime.now(),
            }
        )

        return round_results

    def execute_swarm(
        self,
        initial_input: Any,
        num_rounds: int = 5,
        convergence_function: Optional[Callable[[List[Any]], bool]] = None,
    ) -> List[List[Any]]:
        """Execute multiple rounds until convergence or max rounds."""
        all_results = []

        for round_num in range(num_rounds):
            round_results = self.execute_round(initial_input)
            all_results.append(round_results)

            if convergence_function and convergence_function(round_results):
                break

        return all_results

    def get_swarm_metrics(self) -> Dict[str, Any]:
        """Get swarm metrics."""
        return {
            "swarm_size": len(self.agents),
            "rounds_executed": len(self.execution_rounds),
            "shared_state_size": len(self.shared_state),
        }


# Demo function
def demo():
    """Demonstrate orchestration patterns."""
    from day1.simple_reflex.agent import SimpleReflexAgent

    print("=== Orchestration Patterns Demo ===\n")

    # Centralized
    print("--- Centralized Orchestrator ---")
    central = CentralizedOrchestrator()
    central.register_agent("agent1", SimpleReflexAgent())
    result = central.execute("hello")
    print(f"Result: {result}")
    print(f"Metrics: {central.get_metrics()}\n")

    # Hierarchical
    print("--- Hierarchical Orchestrator ---")
    root = SimpleReflexAgent()
    root.name = "RootAgent"
    hierarchical = HierarchicalOrchestrator(root)

    sub1 = SimpleReflexAgent()
    sub1.name = "SubAgent1"
    hierarchical.add_subordinate("RootAgent", sub1)

    result = hierarchical.execute("help")
    print(f"Result: {result}\n")

    # Decentralized
    print("--- Decentralized Orchestrator ---")
    decentral = DecentralizedOrchestrator()

    agent_a = SimpleReflexAgent()
    agent_a.name = "AgentA"
    agent_b = SimpleReflexAgent()
    agent_b.name = "AgentB"

    decentral.register_agent("AgentA", agent_a)
    decentral.register_agent("AgentB", agent_b)
    decentral.connect_agents("AgentA", "AgentB")

    result = decentral.send_message("AgentA", "AgentB", "hello")
    print(f"Message result: {result}")
    print(f"Network metrics: {decentral.get_network_metrics()}\n")

    # Swarm
    print("--- Swarm Orchestrator ---")
    swarm = SwarmOrchestrator()

    for i in range(3):
        agent = SimpleReflexAgent()
        agent.name = f"SwarmAgent{i+1}"
        swarm.add_agent(agent)

    results = swarm.execute_swarm("hello", num_rounds=2)
    print(f"Swarm results: {len(results)} rounds")
    print(f"Swarm metrics: {swarm.get_swarm_metrics()}")


if __name__ == "__main__":
    demo()
