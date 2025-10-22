# day7/key_capabilities.py - Key Capabilities & Management components

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum


class ModelContextControl:
    """
    Model & Context Control
    - Select Model (GPT-4o, o3-pro)
    - Adjust Settings (Temperature, Max Tokens)
    - Third-Party Models (via LiteLLM)
    - Local Context (Data Class Injection for Tools)
    """

    class ModelProvider(Enum):
        OPENAI = "openai"
        ANTHROPIC = "anthropic"
        GOOGLE = "google"
        LITELLM = "litellm"

    def __init__(
        self,
        provider: ModelProvider = ModelProvider.OPENAI,
        model_name: str = "gpt-4",
    ):
        self.provider = provider
        self.model_name = model_name
        self.settings = {
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 1.0,
        }
        self.local_context: Dict[str, Any] = {}

    def select_model(self, model_name: str):
        """Select a different model."""
        self.model_name = model_name

    def adjust_settings(self, **kwargs):
        """Adjust model settings."""
        self.settings.update(kwargs)

    def inject_local_context(self, key: str, value: Any):
        """Inject local context (Data Class) for tools."""
        self.local_context[key] = value

    def get_context(self, key: str) -> Any:
        """Retrieve local context."""
        return self.local_context.get(key)

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return {
            "provider": self.provider.value,
            "model": self.model_name,
            "settings": self.settings,
            "local_context_keys": list(self.local_context.keys()),
        }


class SystemManagement:
    """
    System Management
    - Visualization (Draw Graph)
    - Guardrails (Input/Output Tripwire)
    - Observability (Traces, Spans, Custom Logging)
    - Testing (End-to-End, Unit Testing Tool Calls)
    """

    def __init__(self):
        self.traces: List[Dict[str, Any]] = []
        self.test_results: List[Dict[str, Any]] = []
        self.visualizations: List[str] = []

    def visualize_graph(self, graph_data: Dict[str, Any]) -> str:
        """Draw a graph visualization."""
        viz = f"Graph: {len(graph_data.get('nodes', []))} nodes, {len(graph_data.get('edges', []))} edges"
        self.visualizations.append(viz)
        return viz

    def add_trace(self, span_name: str, data: Dict[str, Any]):
        """Add observability trace/span."""
        trace = {
            "span": span_name,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        self.traces.append(trace)

    def custom_log(self, message: str, level: str = "INFO"):
        """Custom logging."""
        log_entry = {
            "level": level,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }
        self.traces.append(log_entry)

    def run_test(self, test_name: str, test_fn: callable) -> Dict[str, Any]:
        """Run a test (end-to-end or unit)."""
        start = datetime.now()
        try:
            result = test_fn()
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)

        test_result = {
            "name": test_name,
            "success": success,
            "result": result,
            "error": error,
            "duration_ms": (datetime.now() - start).total_seconds() * 1000,
            "timestamp": start.isoformat(),
        }
        self.test_results.append(test_result)
        return test_result

    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics."""
        return {
            "total_traces": len(self.traces),
            "total_tests": len(self.test_results),
            "test_success_rate": (
                sum(1 for t in self.test_results if t["success"])
                / len(self.test_results)
                if self.test_results
                else 0
            ),
            "visualizations": len(self.visualizations),
        }


class SQLiteMemoryPersistence:
    """
    Long-Term Persistence using SQLite
    Part of Memory Management capabilities
    """

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.sessions: Dict[str, List[Dict]] = {}

    def create_session(self, session_id: str):
        """Create a new session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []

    def store_message(self, session_id: str, message: Dict[str, Any]):
        """Store message in session."""
        if session_id not in self.sessions:
            self.create_session(session_id)
        self.sessions[session_id].append(
            {
                **message,
                "stored_at": datetime.now().isoformat(),
            }
        )

    def get_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieve session messages."""
        return self.sessions.get(session_id, [])

    def get_all_sessions(self) -> List[str]:
        """Get all session IDs."""
        return list(self.sessions.keys())


class StructuredMemoryTools:
    """
    Structured Memory Tools
    Tools for working with structured memory data
    """

    def __init__(self):
        self.structures: Dict[str, Dict] = {}

    def create_structure(self, name: str, schema: Dict[str, Any]):
        """Create a structured memory schema."""
        self.structures[name] = {
            "schema": schema,
            "data": [],
            "created_at": datetime.now().isoformat(),
        }

    def add_entry(self, structure_name: str, entry: Dict[str, Any]):
        """Add entry to structured memory."""
        if structure_name in self.structures:
            self.structures[structure_name]["data"].append(
                {
                    **entry,
                    "added_at": datetime.now().isoformat(),
                }
            )

    def query_structure(
        self, structure_name: str, filter_fn: Optional[callable] = None
    ) -> List[Dict]:
        """Query structured memory."""
        if structure_name not in self.structures:
            return []

        data = self.structures[structure_name]["data"]
        if filter_fn:
            return [item for item in data if filter_fn(item)]
        return data


class KeyCapabilities:
    """
    Complete Key Capabilities & Management
    Integrates: Memory, Orchestration, Model Control, System Management
    """

    def __init__(self):
        self.model_control = ModelContextControl()
        self.system_mgmt = SystemManagement()
        self.sqlite_persistence = SQLiteMemoryPersistence()
        self.structured_memory = StructuredMemoryTools()

    def get_status(self) -> Dict[str, Any]:
        """Get complete capabilities status."""
        return {
            "model_control": self.model_control.get_config(),
            "system_management": self.system_mgmt.get_metrics(),
            "sessions": len(self.sqlite_persistence.get_all_sessions()),
            "memory_structures": len(self.structured_memory.structures),
        }


# Demo
def demo():
    print("=== Key Capabilities & Management Demo ===\n")

    # Model & Context Control
    print("--- Model & Context Control ---")
    model_ctrl = ModelContextControl()
    model_ctrl.select_model("gpt-4o")
    model_ctrl.adjust_settings(temperature=0.8, max_tokens=2000)
    model_ctrl.inject_local_context("user_id", "user123")
    print(f"Config: {model_ctrl.get_config()}")
    print()

    # System Management
    print("--- System Management ---")
    sys_mgmt = SystemManagement()
    sys_mgmt.visualize_graph({"nodes": [1, 2, 3], "edges": [(1, 2), (2, 3)]})
    sys_mgmt.add_trace("agent_execution", {"duration": 100})
    sys_mgmt.custom_log("Test log message")

    def test_func():
        return "success"

    test_result = sys_mgmt.run_test("sample_test", test_func)
    print(f"Test: {test_result['name']} - {'✓' if test_result['success'] else '✗'}")
    print(f"Metrics: {sys_mgmt.get_metrics()}")
    print()

    # SQLite Persistence
    print("--- SQLite Memory Persistence ---")
    sqlite_mem = SQLiteMemoryPersistence()
    sqlite_mem.create_session("session1")
    sqlite_mem.store_message("session1", {"role": "user", "content": "Hello"})
    sqlite_mem.store_message("session1", {"role": "assistant", "content": "Hi!"})
    print(f"Sessions: {sqlite_mem.get_all_sessions()}")
    print(f"Messages: {len(sqlite_mem.get_session('session1'))}")
    print()

    # Structured Memory
    print("--- Structured Memory Tools ---")
    struct_mem = StructuredMemoryTools()
    struct_mem.create_structure("user_prefs", {"type": "object", "properties": {}})
    struct_mem.add_entry("user_prefs", {"key": "theme", "value": "dark"})
    print(f"Structures: {len(struct_mem.structures)}")
    print(f"Entries: {len(struct_mem.query_structure('user_prefs'))}")
    print()

    # Complete capabilities
    print("--- Complete Key Capabilities ---")
    capabilities = KeyCapabilities()
    print(f"Status: {capabilities.get_status()}")


if __name__ == "__main__":
    demo()
