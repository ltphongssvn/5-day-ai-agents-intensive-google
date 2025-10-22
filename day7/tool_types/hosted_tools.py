# day7/tool_types/hosted_tools.py - Hosted Tools (WebSearch, FileSearch, CodeInterpreter)

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum


class HostedToolType(Enum):
    """Types of hosted tools."""

    WEB_SEARCH = "web_search"
    FILE_SEARCH = "file_search"
    CODE_INTERPRETER = "code_interpreter"


class HostedTool:
    """Base class for hosted tools."""

    def __init__(self, name: str, tool_type: HostedToolType):
        self.name = name
        self.tool_type = tool_type
        self.call_history: List[Dict[str, Any]] = []

    def execute(self, **kwargs) -> Any:
        """Execute the tool."""
        raise NotImplementedError

    def log_call(self, input_data: Dict, result: Any, success: bool = True):
        """Log tool call."""
        self.call_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "input": input_data,
                "result": result if success else None,
                "success": success,
            }
        )

    def get_call_history(self) -> List[Dict[str, Any]]:
        """Get call history."""
        return self.call_history.copy()


class WebSearchTool(HostedTool):
    """
    Web Search Tool - Search the web for information.
    """

    def __init__(self, max_results: int = 5):
        super().__init__("web_search", HostedToolType.WEB_SEARCH)
        self.max_results = max_results

    def execute(self, query: str, max_results: Optional[int] = None) -> Dict[str, Any]:
        """Execute web search."""
        num_results = max_results or self.max_results

        # Mock implementation
        results = [
            {
                "title": f"Result {i+1} for '{query}'",
                "url": f"https://example.com/result{i+1}",
                "snippet": f"This is search result {i+1} about {query}...",
            }
            for i in range(num_results)
        ]

        output = {
            "query": query,
            "results": results,
            "total_results": num_results,
        }

        self.log_call({"query": query, "max_results": num_results}, output)
        return output

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI tool schema."""
        return {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web for information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query",
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return",
                        },
                    },
                    "required": ["query"],
                },
            },
        }


class FileSearchTool(HostedTool):
    """
    File Search Tool - Search through files and documents.
    """

    def __init__(self):
        super().__init__("file_search", HostedToolType.FILE_SEARCH)
        self.indexed_files: Dict[str, str] = {}

    def index_file(self, file_id: str, content: str):
        """Index a file for searching."""
        self.indexed_files[file_id] = content

    def execute(
        self, query: str, file_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Execute file search."""
        search_files = file_ids or list(self.indexed_files.keys())
        results = []

        for file_id in search_files:
            if file_id in self.indexed_files:
                content = self.indexed_files[file_id]
                if query.lower() in content.lower():
                    results.append(
                        {
                            "file_id": file_id,
                            "snippet": content[:200],
                            "relevance_score": 0.8,
                        }
                    )

        output = {
            "query": query,
            "results": results,
            "total_results": len(results),
        }

        self.log_call({"query": query, "file_ids": file_ids}, output)
        return output

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI tool schema."""
        return {
            "type": "function",
            "function": {
                "name": "file_search",
                "description": "Search through indexed files",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query",
                        },
                        "file_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of file IDs to search",
                        },
                    },
                    "required": ["query"],
                },
            },
        }


class CodeInterpreterTool(HostedTool):
    """
    Code Interpreter Tool - Execute code and return results.
    """

    def __init__(self, allowed_languages: List[str] = None):
        super().__init__("code_interpreter", HostedToolType.CODE_INTERPRETER)
        self.allowed_languages = allowed_languages or ["python"]

    def execute(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code (mock implementation)."""
        if language not in self.allowed_languages:
            output = {
                "success": False,
                "error": f"Language '{language}' not supported",
            }
            self.log_call({"code": code, "language": language}, output, success=False)
            return output

        # Mock execution
        output = {
            "success": True,
            "language": language,
            "code": code,
            "output": "# Mock execution result\n# Code executed successfully\n# Output: [Simulated result]",
            "execution_time_ms": 42,
        }

        self.log_call({"code": code, "language": language}, output)
        return output

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI tool schema."""
        return {
            "type": "function",
            "function": {
                "name": "code_interpreter",
                "description": "Execute code and return results",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The code to execute",
                        },
                        "language": {
                            "type": "string",
                            "enum": self.allowed_languages,
                            "description": "Programming language",
                        },
                    },
                    "required": ["code"],
                },
            },
        }


# Demo function
def demo():
    """Demonstrate hosted tools."""
    print("=== Hosted Tools Demo ===\n")

    # Web Search Tool
    print("--- Web Search Tool ---")
    web_search = WebSearchTool(max_results=3)
    result = web_search.execute("artificial intelligence")
    print(f"Query: {result['query']}")
    print(f"Results found: {result['total_results']}")
    for i, res in enumerate(result["results"], 1):
        print(f"  {i}. {res['title']}")

    # File Search Tool
    print("\n--- File Search Tool ---")
    file_search = FileSearchTool()
    file_search.index_file("doc1", "This document contains information about AI agents")
    file_search.index_file("doc2", "This is about machine learning algorithms")

    result = file_search.execute("agents")
    print(f"Query: {result['query']}")
    print(f"Results found: {result['total_results']}")
    for res in result["results"]:
        print(f"  File: {res['file_id']}")
        print(f"  Snippet: {res['snippet'][:50]}...")

    # Code Interpreter Tool
    print("\n--- Code Interpreter Tool ---")
    code_interp = CodeInterpreterTool()
    result = code_interp.execute("print('Hello, World!')", "python")
    print(f"Language: {result['language']}")
    print(f"Success: {result['success']}")
    print(f"Output: {result['output'][:80]}...")

    # Show schemas
    print("\n--- OpenAI Tool Schemas ---")
    print(f"Web Search: {web_search.to_openai_schema()['function']['name']}")
    print(f"File Search: {file_search.to_openai_schema()['function']['name']}")
    print(f"Code Interpreter: {code_interp.to_openai_schema()['function']['name']}")

    # Call history
    print("\n--- Call History ---")
    print(f"Web search calls: {len(web_search.get_call_history())}")
    print(f"File search calls: {len(file_search.get_call_history())}")
    print(f"Code interpreter calls: {len(code_interp.get_call_history())}")


if __name__ == "__main__":
    demo()
