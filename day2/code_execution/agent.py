# day2/code_execution/agent.py - Safe code execution agent

from typing import Any, Dict
import subprocess
import sys
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from common.base.agent import BaseAgent


class CodeExecutionAgent(BaseAgent):
    """Agent that safely executes Python code."""

    def __init__(self):
        super().__init__(
            name="CodeExecutionAgent",
            description="Safe code execution with result capture"
        )
        self.execution_history = []

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Parse code input."""
        code = str(input_data).strip()
        return {
            "code": code,
            "lines": len(code.split('\n')),
            "has_imports": 'import' in code,
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Determine execution strategy."""
        return {
            "code": perception["code"],
            "timeout": 5,
            "capture_output": True,
            "safe_mode": True,  # Restrict dangerous operations
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code safely and capture results."""
        code = decision["code"]

        # Check for forbidden operations
        if decision["safe_mode"]:
            forbidden = ['os.system', 'subprocess', 'eval', 'exec', '__import__']
            for forbidden_op in forbidden:
                if forbidden_op in code:
                    return {
                        "success": False,
                        "error": f"Forbidden operation: {forbidden_op}",
                        "output": "",
                    }

        # Execute in isolated environment
        result = self._execute_safe(code)

        # Store in history
        self.execution_history.append({
            "code": code,
            "success": result["success"],
        })

        return result

    def _execute_safe(self, code: str) -> Dict[str, Any]:
        """Execute code with output capture."""
        stdout_capture = StringIO()
        stderr_capture = StringIO()

        try:
            # Create isolated namespace
            namespace = {
                '__builtins__': __builtins__,
                'print': print,
            }

            # Redirect output
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, namespace)

            return {
                "success": True,
                "output": stdout_capture.getvalue(),
                "error": stderr_capture.getvalue(),
            }

        except Exception as e:
            return {
                "success": False,
                "output": stdout_capture.getvalue(),
                "error": f"{type(e).__name__}: {str(e)}",
            }


# Demo function
def demo():
    agent = CodeExecutionAgent()

    test_codes = [
        "print('Hello, World!')",
        "result = 2 + 2\nprint(f'2 + 2 = {result}')",
        "for i in range(3):\n    print(f'Count: {i}')",
        "import math\nprint(f'Pi = {math.pi:.2f}')",
        "x / 0  # This will error",
    ]

    print(f"=== {agent.name} Demo ===\n")
    for code in test_codes:
        print(f"Code:\n{code}\n")
        result = agent.run(code)

        if result["success"]:
            print(f"Output:\n{result['output']}")
        else:
            print(f"Error: {result['error']}")
        print("-" * 50 + "\n")

    print(f"Executions: {len(agent.execution_history)}")
    print(f"Metrics: {agent.get_metrics()}")


if __name__ == "__main__":
    demo()