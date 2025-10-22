# day7/tool_types/mcp_servers.py - MCP (Model Context Protocol) Servers

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum


class MCPResourceType(Enum):
    """Types of MCP resources."""

    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    DATA = "data"


class MCPResource:
    """Represents a resource in MCP."""

    def __init__(
        self,
        uri: str,
        name: str,
        resource_type: MCPResourceType,
        content: Any,
        metadata: Optional[Dict] = None,
    ):
        self.uri = uri
        self.name = name
        self.resource_type = resource_type
        self.content = content
        self.metadata = metadata or {}
        self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "uri": self.uri,
            "name": self.name,
            "type": self.resource_type.value,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


class MCPTool:
    """Represents a tool exposed via MCP."""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable,
    ):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler
        self.call_count = 0

    def execute(self, **kwargs) -> Any:
        """Execute the tool."""
        self.call_count += 1
        return self.handler(**kwargs)

    def to_schema(self) -> Dict[str, Any]:
        """Convert to MCP tool schema."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }


class MCPServer:
    """
    MCP (Model Context Protocol) Server
    Exposes tools and resources for discovery and use by agents.
    """

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.tools: Dict[str, MCPTool] = {}
        self.resources: Dict[str, MCPResource] = {}
        self.prompts: Dict[str, str] = {}
        self.created_at = datetime.now()

    def register_tool(self, tool: MCPTool):
        """Register a tool with the server."""
        self.tools[tool.name] = tool

    def register_resource(self, resource: MCPResource):
        """Register a resource with the server."""
        self.resources[resource.uri] = resource

    def register_prompt(self, name: str, template: str):
        """Register a prompt template."""
        self.prompts[name] = template

    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools."""
        return [tool.to_schema() for tool in self.tools.values()]

    def list_resources(self) -> List[Dict[str, Any]]:
        """List available resources."""
        return [resource.to_dict() for resource in self.resources.values()]

    def list_prompts(self) -> List[Dict[str, str]]:
        """List available prompts."""
        return [
            {"name": name, "template": template}
            for name, template in self.prompts.items()
        ]

    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Call a tool by name."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")

        tool = self.tools[tool_name]
        return tool.execute(**kwargs)

    def get_resource(self, uri: str) -> Optional[MCPResource]:
        """Get a resource by URI."""
        return self.resources.get(uri)

    def get_prompt(self, prompt_name: str, **variables) -> str:
        """Get a prompt template with variables filled."""
        if prompt_name not in self.prompts:
            raise ValueError(f"Prompt '{prompt_name}' not found")

        template = self.prompts[prompt_name]
        return template.format(**variables)

    def get_server_info(self) -> Dict[str, Any]:
        """Get server information."""
        return {
            "name": self.name,
            "description": self.description,
            "tools": len(self.tools),
            "resources": len(self.resources),
            "prompts": len(self.prompts),
            "created_at": self.created_at.isoformat(),
        }


class MCPClient:
    """
    MCP Client for connecting to MCP servers.
    """

    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}

    def connect_server(self, server: MCPServer):
        """Connect to an MCP server."""
        self.servers[server.name] = server

    def discover_tools(
        self, server_name: Optional[str] = None
    ) -> Dict[str, List[Dict]]:
        """Discover tools from connected servers."""
        if server_name:
            if server_name not in self.servers:
                return {}
            return {server_name: self.servers[server_name].list_tools()}

        return {name: server.list_tools() for name, server in self.servers.items()}

    def discover_resources(
        self, server_name: Optional[str] = None
    ) -> Dict[str, List[Dict]]:
        """Discover resources from connected servers."""
        if server_name:
            if server_name not in self.servers:
                return {}
            return {server_name: self.servers[server_name].list_resources()}

        return {name: server.list_resources() for name, server in self.servers.items()}

    def call_tool(self, server_name: str, tool_name: str, **kwargs) -> Any:
        """Call a tool on a specific server."""
        if server_name not in self.servers:
            raise ValueError(f"Server '{server_name}' not connected")

        return self.servers[server_name].call_tool(tool_name, **kwargs)


# Demo function
def demo():
    """Demonstrate MCP servers."""
    print("=== MCP (Model Context Protocol) Demo ===\n")

    # Create MCP server
    server = MCPServer("demo_server", "Demo MCP server with tools and resources")

    # Register tools
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    def calculate(operation: str, a: float, b: float) -> float:
        ops = {"add": lambda x, y: x + y, "multiply": lambda x, y: x * y}
        return ops.get(operation, lambda x, y: 0)(a, b)

    greet_tool = MCPTool(
        name="greet",
        description="Greet a person by name",
        input_schema={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
        handler=greet,
    )

    calc_tool = MCPTool(
        name="calculate",
        description="Perform calculations",
        input_schema={
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["add", "multiply"]},
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "required": ["operation", "a", "b"],
        },
        handler=calculate,
    )

    server.register_tool(greet_tool)
    server.register_tool(calc_tool)

    # Register resources
    doc_resource = MCPResource(
        uri="mcp://docs/readme",
        name="README",
        resource_type=MCPResourceType.TEXT,
        content="This is the README documentation",
        metadata={"version": "1.0"},
    )

    server.register_resource(doc_resource)

    # Register prompts
    server.register_prompt("greeting", "Hello {name}, welcome to {location}!")

    # Create MCP client
    client = MCPClient()
    client.connect_server(server)

    # Discover tools
    print("--- Tool Discovery ---")
    tools = client.discover_tools()
    for server_name, tool_list in tools.items():
        print(f"Server: {server_name}")
        for tool in tool_list:
            print(f"  - {tool['name']}: {tool['description']}")

    # Discover resources
    print("\n--- Resource Discovery ---")
    resources = client.discover_resources()
    for server_name, resource_list in resources.items():
        print(f"Server: {server_name}")
        for resource in resource_list:
            print(f"  - {resource['name']} ({resource['type']})")

    # Call tools
    print("\n--- Tool Execution ---")
    result1 = client.call_tool("demo_server", "greet", name="Alice")
    print(f"greet(Alice): {result1}")

    result2 = client.call_tool("demo_server", "calculate", operation="add", a=10, b=5)
    print(f"calculate(add, 10, 5): {result2}")

    # Use prompts
    print("\n--- Prompt Templates ---")
    prompt = server.get_prompt("greeting", name="Bob", location="MCP World")
    print(f"Prompt: {prompt}")

    # Server info
    print("\n--- Server Info ---")
    info = server.get_server_info()
    for key, value in info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    demo()
