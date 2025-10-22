# day7/tool_types/custom_tools.py - Custom Tools with Pydantic validation

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from pydantic import BaseModel, Field, validator
import json


class ToolParameter(BaseModel):
    """Schema for tool parameters using Pydantic."""

    name: str
    type: str
    description: str
    required: bool = True
    enum: Optional[List[str]] = None


class CustomTool:
    """
    Custom Tool implementation with Pydantic input validation.
    Demonstrates how to create tools that can be used by OpenAI agents.
    """

    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: List[ToolParameter],
    ):
        self.name = name
        self.description = description
        self.function = function
        self.parameters = parameters
        self.call_history: List[Dict[str, Any]] = []

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert tool to OpenAI function calling schema."""
        properties = {}
        required_params = []

        for param in self.parameters:
            prop = {
                "type": param.type,
                "description": param.description,
            }
            if param.enum:
                prop["enum"] = param.enum

            properties[param.name] = prop

            if param.required:
                required_params.append(param.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_params,
                },
            },
        }

    def execute(self, **kwargs) -> Any:
        """Execute the tool function with given arguments."""
        timestamp = datetime.now()

        try:
            result = self.function(**kwargs)

            self.call_history.append(
                {
                    "timestamp": timestamp,
                    "arguments": kwargs,
                    "result": result,
                    "success": True,
                }
            )

            return result

        except Exception as e:
            self.call_history.append(
                {
                    "timestamp": timestamp,
                    "arguments": kwargs,
                    "error": str(e),
                    "success": False,
                }
            )
            raise e

    def get_call_history(self) -> List[Dict[str, Any]]:
        """Return tool call history."""
        return self.call_history.copy()


# Example Custom Tools


class WeatherInput(BaseModel):
    """Pydantic model for weather tool input validation."""

    location: str = Field(..., description="City name")
    unit: str = Field(default="celsius", description="Temperature unit")

    @validator("unit")
    def validate_unit(cls, v):
        if v not in ["celsius", "fahrenheit"]:
            raise ValueError("unit must be celsius or fahrenheit")
        return v


def get_weather_function(location: str, unit: str = "celsius") -> str:
    """Get weather for a location."""
    weather_data = {
        "San Francisco": {"celsius": "15°C", "fahrenheit": "59°F"},
        "New York": {"celsius": "10°C", "fahrenheit": "50°F"},
        "London": {"celsius": "12°C", "fahrenheit": "54°F"},
        "Tokyo": {"celsius": "18°C", "fahrenheit": "64°F"},
    }

    temp = weather_data.get(location, {}).get(unit, "Unknown")
    return f"Weather in {location}: {temp}"


def create_weather_tool() -> CustomTool:
    """Factory function to create weather tool."""
    return CustomTool(
        name="get_weather",
        description="Get current weather for a location",
        function=get_weather_function,
        parameters=[
            ToolParameter(
                name="location",
                type="string",
                description="The city name (e.g., San Francisco)",
                required=True,
            ),
            ToolParameter(
                name="unit",
                type="string",
                description="Temperature unit",
                required=False,
                enum=["celsius", "fahrenheit"],
            ),
        ],
    )


class CalculatorInput(BaseModel):
    """Pydantic model for calculator input."""

    operation: str = Field(..., description="Math operation")
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")

    @validator("operation")
    def validate_operation(cls, v):
        if v not in ["add", "subtract", "multiply", "divide"]:
            raise ValueError("operation must be add, subtract, multiply, or divide")
        return v


def calculator_function(operation: str, a: float, b: float) -> float:
    """Perform basic math operations."""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else float("inf"),
    }

    result = operations[operation](a, b)
    return result


def create_calculator_tool() -> CustomTool:
    """Factory function to create calculator tool."""
    return CustomTool(
        name="calculator",
        description="Perform basic mathematical operations",
        function=calculator_function,
        parameters=[
            ToolParameter(
                name="operation",
                type="string",
                description="Math operation to perform",
                required=True,
                enum=["add", "subtract", "multiply", "divide"],
            ),
            ToolParameter(
                name="a",
                type="number",
                description="First number",
                required=True,
            ),
            ToolParameter(
                name="b",
                type="number",
                description="Second number",
                required=True,
            ),
        ],
    )


# Demo function
def demo():
    """Demonstrate custom tools."""
    print("=== Custom Tools Demo ===\n")

    # Create tools
    weather_tool = create_weather_tool()
    calc_tool = create_calculator_tool()

    print("--- Weather Tool ---")
    print(f"Name: {weather_tool.name}")
    print(f"Description: {weather_tool.description}")
    print("\nOpenAI Schema:")
    print(json.dumps(weather_tool.to_openai_schema(), indent=2))

    print("\nExecuting weather tool:")
    result1 = weather_tool.execute(location="San Francisco", unit="celsius")
    print(f"Result: {result1}")

    result2 = weather_tool.execute(location="Tokyo", unit="fahrenheit")
    print(f"Result: {result2}")

    print("\n--- Calculator Tool ---")
    print(f"Name: {calc_tool.name}")
    print(f"Description: {calc_tool.description}")

    print("\nExecuting calculator tool:")
    result3 = calc_tool.execute(operation="add", a=10, b=5)
    print(f"10 + 5 = {result3}")

    result4 = calc_tool.execute(operation="multiply", a=7, b=8)
    print(f"7 * 8 = {result4}")

    print("\n--- Tool Call History ---")
    print(f"Weather calls: {len(weather_tool.get_call_history())}")
    print(f"Calculator calls: {len(calc_tool.get_call_history())}")


if __name__ == "__main__":
    demo()
