# day7/agent_anatomy.py - AI Agent Anatomy & Design structure

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum


class ModelConfig:
    """
    Model (The Brain)
    - LLM selection
    - Trade-offs: Cost, Latency, Performance, Bias
    - System Prompt (Identity/Purpose)
    """

    def __init__(
        self,
        llm_provider: str = "openai",
        model_name: str = "gpt-4",
        system_prompt: str = "You are a helpful AI assistant.",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Track trade-offs
        self.trade_offs = self._calculate_trade_offs()

    def _calculate_trade_offs(self) -> Dict[str, str]:
        """Calculate model trade-offs."""
        trade_offs = {
            "cost": "medium",
            "latency": "medium",
            "performance": "high",
            "bias": "low",
        }

        # Adjust based on model
        if "gpt-4" in self.model_name:
            trade_offs.update({"cost": "high", "performance": "very high"})
        elif "gpt-3.5" in self.model_name:
            trade_offs.update({"cost": "low", "latency": "low"})
        elif "gemini" in self.model_name.lower():
            trade_offs.update({"cost": "medium", "performance": "high"})

        return trade_offs

    def get_info(self) -> Dict[str, Any]:
        """Get model configuration info."""
        return {
            "provider": self.llm_provider,
            "model": self.model_name,
            "system_prompt": self.system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "trade_offs": self.trade_offs,
        }


class ToolingInterface:
    """
    Tooling Interface (Hands/Eyes)
    - Interacts with Outside World (APIs, Functions)
    - Tool Registration/Execution
    """

    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: Dict[str, Dict] = {}
        self.execution_log: List[Dict[str, Any]] = []

    def register_tool(
        self,
        name: str,
        function: Callable,
        schema: Dict[str, Any],
    ):
        """Register a tool for the agent."""
        self.tools[name] = function
        self.tool_schemas[name] = schema

    def execute_tool(self, name: str, **kwargs) -> Any:
        """Execute a registered tool."""
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not registered")

        start_time = datetime.now()
        result = self.tools[name](**kwargs)

        self.execution_log.append(
            {
                "tool": name,
                "arguments": kwargs,
                "result": result,
                "timestamp": start_time,
                "duration_ms": (datetime.now() - start_time).total_seconds() * 1000,
            }
        )

        return result

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        return list(self.tools.keys())

    def get_tool_schema(self, name: str) -> Dict[str, Any]:
        """Get schema for a tool."""
        return self.tool_schemas.get(name, {})


class MemoryKnowledge:
    """
    Memory & Knowledge (Reference Textbook)
    - Working Memory (Short-Term/Session History)
    - Long-Term Memory (Persistent Storage/Database)
    - Training Knowledge (Baked-in Knowledge)
    - Retrieved Knowledge (RAG/Vector Search)
    """

    def __init__(self, max_working_memory: int = 10):
        self.working_memory: List[Dict[str, Any]] = []
        self.long_term_storage: Dict[str, Any] = {}
        self.max_working_memory = max_working_memory

        # Knowledge sources
        self.training_knowledge = "Model's pre-trained knowledge"
        self.retrieved_knowledge: List[Dict[str, Any]] = []

    def add_to_working_memory(self, item: Dict[str, Any]):
        """Add item to working memory (session history)."""
        self.working_memory.append(
            {
                **item,
                "timestamp": datetime.now(),
            }
        )

        # Trim if exceeds max
        if len(self.working_memory) > self.max_working_memory:
            self.working_memory.pop(0)

    def store_long_term(self, key: str, value: Any):
        """Store in long-term memory (persistent)."""
        self.long_term_storage[key] = {
            "value": value,
            "stored_at": datetime.now(),
        }

    def retrieve_long_term(self, key: str) -> Optional[Any]:
        """Retrieve from long-term memory."""
        item = self.long_term_storage.get(key)
        return item["value"] if item else None

    def add_retrieved_knowledge(self, knowledge: Dict[str, Any]):
        """Add RAG/vector search results."""
        self.retrieved_knowledge.append(
            {
                **knowledge,
                "retrieved_at": datetime.now(),
            }
        )

    def get_context(self) -> Dict[str, Any]:
        """Get full memory context."""
        return {
            "working_memory": self.working_memory,
            "long_term_count": len(self.long_term_storage),
            "retrieved_knowledge_count": len(self.retrieved_knowledge),
            "training_knowledge": self.training_knowledge,
        }


class ControlLogicFramework:
    """
    Control Logic Framework
    - Iterative Loop: Observe, Reason, Act
    - Patterns: CoT, ReAct, Planner-Execution
    """

    class Pattern(Enum):
        OBSERVE_REASON_ACT = "observe_reason_act"
        CHAIN_OF_THOUGHT = "cot"
        REACT = "react"
        PLANNER_EXECUTION = "planner_execution"

    def __init__(self, pattern: Pattern = Pattern.OBSERVE_REASON_ACT):
        self.pattern = pattern
        self.execution_trace: List[Dict[str, Any]] = []

    def observe(self, input_data: Any) -> Any:
        """Observe: Perceive input."""
        observation = {
            "type": "observation",
            "data": input_data,
            "timestamp": datetime.now(),
        }
        self.execution_trace.append(observation)
        return input_data

    def reason(self, observation: Any) -> Any:
        """Reason: Process and decide."""
        reasoning = {
            "type": "reasoning",
            "input": observation,
            "pattern": self.pattern.value,
            "timestamp": datetime.now(),
        }
        self.execution_trace.append(reasoning)
        return reasoning

    def act(self, reasoning: Any) -> Any:
        """Act: Execute action."""
        action = {
            "type": "action",
            "based_on": reasoning,
            "timestamp": datetime.now(),
        }
        self.execution_trace.append(action)
        return action

    def execute_loop(self, input_data: Any) -> Any:
        """Execute full Observe-Reason-Act loop."""
        observation = self.observe(input_data)
        reasoning = self.reason(observation)
        action = self.act(reasoning)
        return action

    def get_trace(self) -> List[Dict[str, Any]]:
        """Get execution trace."""
        return self.execution_trace.copy()


class AgentAnatomy:
    """
    Complete AI Agent Anatomy & Design
    Integrates all 4 components: Model, Tooling, Memory, Control Logic
    """

    def __init__(
        self,
        model_config: Optional[ModelConfig] = None,
        max_working_memory: int = 10,
        control_pattern: ControlLogicFramework.Pattern = ControlLogicFramework.Pattern.OBSERVE_REASON_ACT,
    ):
        # Initialize 4 components
        self.model = model_config or ModelConfig()
        self.tooling = ToolingInterface()
        self.memory = MemoryKnowledge(max_working_memory)
        self.control_logic = ControlLogicFramework(control_pattern)

    def process(self, input_data: Any) -> Dict[str, Any]:
        """Process input through complete agent anatomy."""
        # Control Logic: Observe
        observation = self.control_logic.observe(input_data)

        # Memory: Add to working memory
        self.memory.add_to_working_memory(
            {
                "type": "input",
                "content": observation,
            }
        )

        # Control Logic: Reason
        reasoning = self.control_logic.reason(observation)

        # Control Logic: Act
        action = self.control_logic.act(reasoning)

        return {
            "observation": observation,
            "reasoning": reasoning,
            "action": action,
            "memory_context": self.memory.get_context(),
        }

    def get_anatomy_info(self) -> Dict[str, Any]:
        """Get complete anatomy information."""
        return {
            "model": self.model.get_info(),
            "tooling": {
                "registered_tools": self.tooling.list_tools(),
                "executions": len(self.tooling.execution_log),
            },
            "memory": self.memory.get_context(),
            "control_logic": {
                "pattern": self.control_logic.pattern.value,
                "trace_length": len(self.control_logic.execution_trace),
            },
        }


# Demo function
def demo():
    """Demonstrate AI Agent Anatomy & Design."""
    print("=== AI Agent Anatomy & Design Demo ===\n")

    # Create model config
    print("--- Model (The Brain) ---")
    model = ModelConfig(
        model_name="gpt-4",
        system_prompt="You are a research assistant.",
    )
    print(f"Model: {model.model_name}")
    print(f"Trade-offs: {model.trade_offs}")
    print()

    # Create complete agent anatomy
    print("--- Complete Agent Anatomy ---")
    agent = AgentAnatomy(model_config=model)

    # Register tools
    def search_tool(query: str) -> str:
        return f"Search results for: {query}"

    agent.tooling.register_tool(
        "search", search_tool, {"type": "function", "description": "Search tool"}
    )

    # Process input
    print("Processing input...")
    result = agent.process("What is machine learning?")
    print(f"Observation: {result['observation']}")
    print(f"Memory context: Working={len(result['memory_context']['working_memory'])}")
    print()

    # Show anatomy
    print("--- Agent Anatomy Info ---")
    info = agent.get_anatomy_info()
    print(f"Model: {info['model']['model']}")
    print(f"Tools: {info['tooling']['registered_tools']}")
    print(
        f"Memory: {info['memory']['working_memory'][-1] if info['memory']['working_memory'] else 'empty'}"
    )
    print(f"Control: {info['control_logic']['pattern']}")


if __name__ == "__main__":
    demo()
