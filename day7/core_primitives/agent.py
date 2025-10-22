# day7/core_primitives/agent.py - OpenAI Agents SDK Core Primitive: Agent (LLM Wrapper)
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from openai import OpenAI
from common.base.agent import BaseAgent
from common.config.settings import settings


class OpenAIAgentPrimitive(BaseAgent):
    """
    Core Primitive: Agent

    An LLM wrapper with instructions and tools, demonstrating the fundamental
    building block of the OpenAI Agents SDK.
    """

    def __init__(
        self,
        name: str = "OpenAIAgentPrimitive",
        instructions: str = "You are a helpful AI assistant.",
        model: str = "gpt-4",
        tools: Optional[List[Dict[str, Any]]] = None,
    ):
        super().__init__(
            name=name,
            description="OpenAI Agent primitive with LLM, instructions, and tools",
        )

        if (
            not settings.openai_api_key
            or settings.openai_api_key
            == "your_openai_api_key_here"  # pragma: allowlist secret
        ):
            raise ValueError(
                "OpenAI API key not configured. Please set OPENAI_API_KEY in .env file"
            )

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.instructions = instructions
        self.model = model
        self.tools = tools or []
        self.conversation_history: List[Dict[str, str]] = []

        # Register available tool functions
        self.tool_functions: Dict[str, Callable] = {}

    def register_tool(self, name: str, function: Callable):
        """Register a tool function that can be called by the agent."""
        self.tool_functions[name] = function

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Process user input and maintain conversation context."""
        user_message = str(input_data).strip()

        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})

        return {
            "type": "user_input",
            "content": user_message,
            "timestamp": datetime.now().isoformat(),
        }

    def reason(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use LLM to reason about the input and decide on response.
        This is where the agent's "thinking" happens.
        """
        try:
            # Prepare messages for OpenAI
            messages = [{"role": "system", "content": self.instructions}]
            messages.extend(self.conversation_history)

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools if self.tools else None,
            )

            assistant_message = response.choices[0].message

            # Handle tool calls if present
            if assistant_message.tool_calls:
                return {
                    "type": "tool_call_required",
                    "tool_calls": assistant_message.tool_calls,
                    "response": assistant_message,
                }

            return {
                "type": "direct_response",
                "content": assistant_message.content,
                "response": assistant_message,
            }

        except Exception as e:
            return {"type": "error", "error": str(e)}

    def act(self, reasoning: Dict[str, Any]) -> str:
        """
        Execute the decided action based on reasoning.
        This could be returning a response or calling tools.
        """
        if reasoning["type"] == "error":
            return f"Error: {reasoning['error']}"

        if reasoning["type"] == "tool_call_required":
            # Execute tool calls
            tool_results = []
            for tool_call in reasoning["tool_calls"]:
                tool_name = tool_call.function.name
                if tool_name in self.tool_functions:
                    result = self.tool_functions[tool_name]()
                    tool_results.append(result)

            # Add assistant message and tool results to history
            self.conversation_history.append(
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": reasoning["tool_calls"],
                }
            )

            return f"Tool calls executed: {tool_results}"

        # Direct response
        response_content = reasoning["content"]
        self.conversation_history.append(
            {"role": "assistant", "content": response_content}
        )

        return response_content

    def execute(self, input_data: Any) -> str:
        """
        Main execution loop: Perceive -> Reason -> Act
        This is the agent's core processing pipeline.
        """
        # Step 1: Perceive
        perception = self.perceive(input_data)

        # Step 2: Reason
        reasoning = self.reason(perception)

        # Step 3: Act
        response = self.act(reasoning)

        return response

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history.clear()


# Demo function
def demo():
    """Demonstrate OpenAI Agent primitive with a simple tool."""
    print("=== OpenAI Agent Primitive Demo ===\n")
    print("Note: This demo requires a valid OpenAI API key.")
    print("Set OPENAI_API_KEY in your .env file to run this demo.\n")

    try:
        # Create an agent
        agent = OpenAIAgentPrimitive(
            name="DemoAgent",
            instructions="You are a helpful assistant that can answer questions.",
            model="gpt-4",
        )

        # Register a simple tool
        def get_current_time():
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        agent.register_tool("get_time", get_current_time)

        print("Agent created successfully!")
        print(f"Name: {agent.name}")
        print(f"Model: {agent.model}")
        print(f"Instructions: {agent.instructions}")
        print("\nAgent is ready to process requests.")
        print("(Actual execution requires valid API key and will make API calls)\n")

    except ValueError as e:
        print(f"Cannot create agent: {e}")
        print("\nTo use this agent:")
        print("1. Get an OpenAI API key from https://platform.openai.com")
        print("2. Add it to your .env file: OPENAI_API_KEY=your_key_here")
        print("3. Run this demo again")


if __name__ == "__main__":
    demo()
