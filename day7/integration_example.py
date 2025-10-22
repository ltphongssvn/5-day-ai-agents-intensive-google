# day7/integration_example.py - Complete OpenAI Agents SDK Integration Example

from day7.core_primitives.agent import OpenAIAgentPrimitive
from day7.core_primitives.runner import Runner, ExecutionMode
from day7.tool_types.custom_tools import create_weather_tool, create_calculator_tool
from day7.memory_management.memory import ContextManager
from day7.orchestration.patterns import CentralizedOrchestrator


def integration_demo():
    """
    Complete integration demonstrating all OpenAI Agents SDK components:
    - Core Primitives (Agent, Runner)
    - Tool Types (Custom Tools)
    - Memory Management (Working + Long-term)
    - Control Logic (ReAct, Planner-Executor)
    - Orchestration (Centralized)
    """

    print("=" * 60)
    print("OpenAI Agents SDK - Complete Integration Example")
    print("=" * 60)
    print()

    try:
        # 1. Setup Tools
        print("1. Setting up Custom Tools...")
        weather_tool = create_weather_tool()
        calc_tool = create_calculator_tool()
        print(f"   ✓ Weather tool: {weather_tool.name}")
        print(f"   ✓ Calculator tool: {calc_tool.name}")
        print()

        # 2. Create Agent with Tools
        print("2. Creating OpenAI Agent with Tools...")
        agent = OpenAIAgentPrimitive(
            name="IntegratedAgent",
            instructions="You are a helpful assistant with weather and calculator tools.",
            model="gpt-3.5-turbo",
            tools=[
                weather_tool.to_openai_schema(),
                calc_tool.to_openai_schema(),
            ],
        )
        agent.register_tool("get_weather", weather_tool.function)
        agent.register_tool("calculator", calc_tool.function)
        print(f"   ✓ Agent created: {agent.name}")
        print()

        # 3. Setup Memory
        print("3. Setting up Memory Management...")
        memory = ContextManager(working_memory_size=10)
        memory.store_user_preference("user_name", "Alice")
        memory.store_user_preference("favorite_city", "San Francisco")
        print("   ✓ Context manager initialized")
        print("   ✓ User preferences stored")
        print()

        # 4. Setup Runner
        print("4. Configuring Runner (Execution Engine)...")
        runner = Runner(mode=ExecutionMode.SINGLE)
        print(f"   ✓ Runner mode: {runner.mode.value}")
        print()

        # 5. Execute with different patterns
        print("5. Executing Tasks...")
        print("-" * 60)

        # Simple execution
        print("\n[Task 1: Simple Query]")
        response1 = runner.run(agent, "What's the weather in San Francisco?")
        print(f"Response: {response1}")
        memory.add_interaction(
            "What's the weather in San Francisco?", response1, store_in_long_term=True
        )

        # With calculator
        print("\n[Task 2: Calculation]")
        response2 = runner.run(agent, "Calculate 25 * 8")
        print(f"Response: {response2}")
        memory.add_interaction("Calculate 25 * 8", response2, store_in_long_term=True)

        print()
        print("-" * 60)

        # 6. Show Memory State
        print("\n6. Memory State:")
        print(
            f"   Working memory: {len(memory.working_memory.get_messages())} messages"
        )
        if memory.long_term_memory:
            print(f"   Long-term memory: {len(memory.long_term_memory.facts)} facts")
        print()

        # 7. Show Metrics
        print("7. System Metrics:")
        print(f"   Agent executions: {agent.get_metrics()['total_requests']}")
        print(f"   Runner executions: {runner.get_metrics()['total_executions']}")
        print(f"   Weather tool calls: {len(weather_tool.get_call_history())}")
        print(f"   Calculator calls: {len(calc_tool.get_call_history())}")
        print()

        print("=" * 60)
        print("✓ Integration Demo Complete!")
        print("=" * 60)

    except ValueError as e:
        print(f"\n⚠ Configuration Error: {e}")
        print("\nTo run this integration:")
        print("1. Set OPENAI_API_KEY in your .env file")
        print("2. Ensure the API key is valid")
        print()


def orchestration_demo():
    """Demonstrate multi-agent orchestration."""
    from day1.simple_reflex.agent import SimpleReflexAgent

    print("\n" + "=" * 60)
    print("Multi-Agent Orchestration Example")
    print("=" * 60)
    print()

    # Create orchestrator
    orchestrator = CentralizedOrchestrator("MainOrchestrator")

    # Register agents
    agent1 = SimpleReflexAgent()
    agent1.name = "ReflexAgent"
    orchestrator.register_agent("reflex", agent1)

    # Define routing rule
    def route_by_keyword(task: str) -> str:
        task_lower = str(task).lower()
        if any(word in task_lower for word in ["hello", "hi", "hey"]):
            return "reflex"
        return "reflex"  # default

    orchestrator.register_routing_rule("keyword", route_by_keyword)

    # Execute tasks
    print("Executing tasks through orchestrator...")
    result1 = orchestrator.execute("hello", "keyword")
    print(f"Task 1: {result1}")

    result2 = orchestrator.execute("help", "keyword")
    print(f"Task 2: {result2}")

    print(f"\nOrchestrator metrics: {orchestrator.get_metrics()}")
    print()


if __name__ == "__main__":
    integration_demo()
    orchestration_demo()
