# day7/core_primitives/tools.py - Tools Core Primitive (Functions, Hosted APIs, MCP)

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum


class ToolType(Enum):
    """Types of tools in the framework."""

    FUNCTION = "function"
    HOSTED_API = "hosted_api"
    MCP = "mcp"
    AGENT = "agent"


class Tool:
    """
    Core Primitive: Tools
    Unified interface for Functions, Hosted APIs, and MCP tools.
    """

    def __init__(
        self,
        name: str,
        tool_type: ToolType,
        description: str,
        handler: Callable,
        schema: Dict[str, Any],
    ):
        self.name = name
        self.tool_type = tool_type
        self.description = description
        self.handler = handler
        self.schema = schema
        self.call_history: List[Dict[str, Any]] = []

    def execute(self, **kwargs) -> Any:
        """Execute the tool."""
        start_time = datetime.now()

        try:
            result = self.handler(**kwargs)

            self.call_history.append(
                {
                    "timestamp": start_time.isoformat(),
                    "arguments": kwargs,
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
                    "arguments": kwargs,
                    "error": str(e),
                    "success": False,
                }
            )
            raise e

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.schema,
            },
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Get tool usage metrics."""
        total = len(self.call_history)
        successful = sum(1 for call in self.call_history if call.get("success", False))

        durations = [
            call["duration_ms"] for call in self.call_history if "duration_ms" in call
        ]

        return {
            "name": self.name,
            "type": self.tool_type.value,
            "total_calls": total,
            "successful_calls": successful,
            "failed_calls": total - successful,
            "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
        }


class ToolRegistry:
    """
    Registry for managing all tools (Functions, Hosted APIs, MCP).
    Central hub for tool registration and discovery.
    """

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.tools_by_type: Dict[ToolType, List[Tool]] = {
            ToolType.FUNCTION: [],
            ToolType.HOSTED_API: [],
            ToolType.MCP: [],
            ToolType.AGENT: [],
        }

    def register_tool(self, tool: Tool):
        """Register a tool in the registry."""
        self.tools[tool.name] = tool
        self.tools_by_type[tool.tool_type].append(tool)

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self.tools.get(name)

    def list_tools(self, tool_type: Optional[ToolType] = None) -> List[Tool]:
        """List all tools or tools of a specific type."""
        if tool_type:
            return self.tools_by_type[tool_type].copy()
        return list(self.tools.values())

    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Call a tool by name."""
        tool = self.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found")
        return tool.execute(**kwargs)

    def get_schemas(self) -> List[Dict[str, Any]]:
        """Get OpenAI schemas for all tools."""
        return [tool.to_openai_schema() for tool in self.tools.values()]

    def get_registry_metrics(self) -> Dict[str, Any]:
        """Get registry-wide metrics."""
        return {
            "total_tools": len(self.tools),
            "by_type": {
                tool_type.value: len(tools)
                for tool_type, tools in self.tools_by_type.items()
            },
            "tool_metrics": [tool.get_metrics() for tool in self.tools.values()],
        }


# Factory functions for creating tools


def create_function_tool(
    name: str,
    description: str,
    handler: Callable,
    parameters: Dict[str, Any],
) -> Tool:
    """Create a function tool."""
    return Tool(
        name=name,
        tool_type=ToolType.FUNCTION,
        description=description,
        handler=handler,
        schema=parameters,
    )


def create_hosted_api_tool(
    name: str,
    description: str,
    api_handler: Callable,
    parameters: Dict[str, Any],
) -> Tool:
    """Create a hosted API tool."""
    return Tool(
        name=name,
        tool_type=ToolType.HOSTED_API,
        description=description,
        handler=api_handler,
        schema=parameters,
    )


def create_mcp_tool(
    name: str,
    description: str,
    mcp_handler: Callable,
    parameters: Dict[str, Any],
) -> Tool:
    """Create an MCP protocol tool."""
    return Tool(
        name=name,
        tool_type=ToolType.MCP,
        description=description,
        handler=mcp_handler,
        schema=parameters,
    )


# Demo function
def demo():
    """Demonstrate Tools core primitive."""
    print("=== Tools Core Primitive Demo ===\n")

    # Create registry
    registry = ToolRegistry()

    # Create function tool
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    greet_tool = create_function_tool(
        name="greet",
        description="Greet a person",
        handler=greet,
        parameters={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    )

    # Create hosted API tool
    def search_api(query: str, limit: int = 5) -> Dict:
        return {"query": query, "results": [f"Result {i}" for i in range(limit)]}

    search_tool = create_hosted_api_tool(
        name="search",
        description="Search API",
        api_handler=search_api,
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": ["query"],
        },
    )

    # Create MCP tool
    def mcp_fetch(resource: str) -> str:
        return f"Fetched: {resource}"

    mcp_tool = create_mcp_tool(
        name="mcp_fetch",
        description="Fetch via MCP",
        mcp_handler=mcp_fetch,
        parameters={
            "type": "object",
            "properties": {"resource": {"type": "string"}},
            "required": ["resource"],
        },
    )

    # Register tools
    registry.register_tool(greet_tool)
    registry.register_tool(search_tool)
    registry.register_tool(mcp_tool)

    # Demo tool execution
    print("--- Tool Execution ---")
    result1 = registry.call_tool("greet", name="Alice")
    print(f"greet: {result1}")

    result2 = registry.call_tool("search", query="AI agents", limit=3)
    print(f"search: {result2}")

    result3 = registry.call_tool("mcp_fetch", resource="docs/readme")
    print(f"mcp_fetch: {result3}")

    # List tools by type
    print("\n--- Tools by Type ---")
    for tool_type in ToolType:
        tools = registry.list_tools(tool_type)
        print(f"{tool_type.value}: {len(tools)} tools")
        for tool in tools:
            print(f"  - {tool.name}")

    # Show metrics
    print("\n--- Registry Metrics ---")
    metrics = registry.get_registry_metrics()
    print(f"Total tools: {metrics['total_tools']}")
    print(f"By type: {metrics['by_type']}")

    # Show OpenAI schemas
    print("\n--- OpenAI Schemas ---")
    schemas = registry.get_schemas()
    print(f"Generated {len(schemas)} schemas")
    print(f"Example: {schemas[0]['function']['name']}")


if __name__ == "__main__":
    demo()
