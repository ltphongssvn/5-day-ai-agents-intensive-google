# day7/memory_management/memory.py - Memory Management: Working Memory, Long-Term Memory, Context Management

from typing import Any, Dict, List, Optional
from datetime import datetime
from collections import deque
import json


class WorkingMemory:
    """
    Working Memory (Short-Term Session History)
    Manages conversation context with sliding window and summarization.
    """

    def __init__(
        self,
        max_messages: int = 10,
        enable_sliding_window: bool = True,
    ):
        self.max_messages = max_messages
        self.enable_sliding_window = enable_sliding_window
        self.messages: deque = deque(
            maxlen=max_messages if enable_sliding_window else None
        )
        self.message_count = 0

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to working memory."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "message_id": self.message_count,
            "metadata": metadata or {},
        }

        self.messages.append(message)
        self.message_count += 1

    def get_messages(self, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get messages from working memory."""
        if last_n:
            return list(self.messages)[-last_n:]
        return list(self.messages)

    def get_context(self) -> str:
        """Get formatted context string."""
        context_parts = []
        for msg in self.messages:
            context_parts.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(context_parts)

    def clear(self):
        """Clear working memory."""
        self.messages.clear()

    def summarize(self) -> str:
        """Create a summary of the conversation."""
        if not self.messages:
            return "No conversation history."

        msg_count = len(self.messages)
        first_msg = self.messages[0]
        last_msg = self.messages[-1]

        return f"Conversation summary: {msg_count} messages from {first_msg['timestamp']} to {last_msg['timestamp']}"

    def get_metrics(self) -> Dict[str, Any]:
        """Get memory metrics."""
        return {
            "current_size": len(self.messages),
            "max_size": self.max_messages,
            "total_messages": self.message_count,
            "utilization": (
                len(self.messages) / self.max_messages if self.max_messages else 0
            ),
        }


class LongTermMemory:
    """
    Long-Term Memory (Persistent Storage)
    Stores information across sessions with search and retrieval capabilities.
    """

    def __init__(self):
        self.storage: Dict[str, Any] = {}
        self.facts: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
        }

    def store_fact(self, key: str, value: Any, category: str = "general"):
        """Store a fact in long-term memory."""
        fact = {
            "key": key,
            "value": value,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "access_count": 0,
        }

        self.facts.append(fact)
        self.storage[key] = fact
        self.metadata["last_updated"] = datetime.now().isoformat()

    def retrieve_fact(self, key: str) -> Optional[Any]:
        """Retrieve a fact by key."""
        if key in self.storage:
            fact = self.storage[key]
            fact["access_count"] += 1
            fact["last_accessed"] = datetime.now().isoformat()
            return fact["value"]
        return None

    def search_facts(
        self, query: str, category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search facts by query string."""
        results = []
        query_lower = query.lower()

        for fact in self.facts:
            if category and fact["category"] != category:
                continue

            if (
                query_lower in str(fact["key"]).lower()
                or query_lower in str(fact["value"]).lower()
            ):
                results.append(fact)

        return results

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all facts in a category."""
        return [fact for fact in self.facts if fact["category"] == category]

    def get_recent_facts(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get most recent facts."""
        return sorted(self.facts, key=lambda x: x["timestamp"], reverse=True)[:n]

    def get_frequent_facts(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get most frequently accessed facts."""
        return sorted(self.facts, key=lambda x: x["access_count"], reverse=True)[:n]

    def export_to_json(self) -> str:
        """Export memory to JSON."""
        return json.dumps(
            {
                "facts": self.facts,
                "metadata": self.metadata,
            },
            indent=2,
        )

    def import_from_json(self, json_str: str):
        """Import memory from JSON."""
        data = json.loads(json_str)
        self.facts = data.get("facts", [])
        self.storage = {fact["key"]: fact for fact in self.facts}
        self.metadata = data.get("metadata", self.metadata)

    def get_metrics(self) -> Dict[str, Any]:
        """Get memory metrics."""
        categories = {}
        for fact in self.facts:
            cat = fact["category"]
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "total_facts": len(self.facts),
            "categories": categories,
            "created_at": self.metadata["created_at"],
            "last_updated": self.metadata["last_updated"],
        }


class ContextManager:
    """
    Context Manager
    Combines working and long-term memory with context limiting.
    """

    def __init__(
        self,
        working_memory_size: int = 10,
        enable_long_term: bool = True,
    ):
        self.working_memory = WorkingMemory(max_messages=working_memory_size)
        self.long_term_memory = LongTermMemory() if enable_long_term else None

    def add_interaction(
        self,
        user_message: str,
        agent_response: str,
        store_in_long_term: bool = False,
    ):
        """Add an interaction to memory."""
        self.working_memory.add_message("user", user_message)
        self.working_memory.add_message("assistant", agent_response)

        if store_in_long_term and self.long_term_memory:
            timestamp = datetime.now().isoformat()
            self.long_term_memory.store_fact(
                key=f"interaction_{timestamp}",
                value={"user": user_message, "assistant": agent_response},
                category="conversation",
            )

    def get_context_for_agent(self, include_summary: bool = False) -> str:
        """Get formatted context for agent."""
        context = self.working_memory.get_context()

        if include_summary and self.long_term_memory:
            recent_facts = self.long_term_memory.get_recent_facts(3)
            if recent_facts:
                context += "\n\nRecent facts:\n"
                for fact in recent_facts:
                    context += f"- {fact['key']}: {fact['value']}\n"

        return context

    def store_user_preference(self, key: str, value: Any):
        """Store user preference in long-term memory."""
        if self.long_term_memory:
            self.long_term_memory.store_fact(key, value, category="preference")

    def get_user_preference(self, key: str) -> Optional[Any]:
        """Retrieve user preference."""
        if self.long_term_memory:
            return self.long_term_memory.retrieve_fact(key)
        return None

    def get_full_metrics(self) -> Dict[str, Any]:
        """Get metrics from all memory systems."""
        metrics = {
            "working_memory": self.working_memory.get_metrics(),
        }

        if self.long_term_memory:
            metrics["long_term_memory"] = self.long_term_memory.get_metrics()

        return metrics


# Demo function
def demo():
    """Demonstrate memory management."""
    print("=== Memory Management Demo ===\n")

    # Working Memory Demo
    print("--- Working Memory ---")
    working_mem = WorkingMemory(max_messages=5)

    working_mem.add_message("user", "Hello!")
    working_mem.add_message("assistant", "Hi! How can I help?")
    working_mem.add_message("user", "What's the weather?")
    working_mem.add_message("assistant", "It's sunny today.")

    print(f"Messages: {len(working_mem.get_messages())}")
    print(f"Context:\n{working_mem.get_context()}\n")
    print(f"Metrics: {working_mem.get_metrics()}\n")

    # Long-Term Memory Demo
    print("--- Long-Term Memory ---")
    long_term_mem = LongTermMemory()

    long_term_mem.store_fact("user_name", "Alice", "profile")
    long_term_mem.store_fact("user_city", "San Francisco", "profile")
    long_term_mem.store_fact("favorite_color", "blue", "preference")

    print(f"Retrieved name: {long_term_mem.retrieve_fact('user_name')}")
    print(f"Profile facts: {len(long_term_mem.get_by_category('profile'))}")
    print(f"Metrics: {long_term_mem.get_metrics()}\n")

    # Context Manager Demo
    print("--- Context Manager ---")
    context_mgr = ContextManager(working_memory_size=10)

    context_mgr.add_interaction(
        "What's my name?", "I don't know yet.", store_in_long_term=True
    )
    context_mgr.store_user_preference("user_name", "Bob")

    context_mgr.add_interaction(
        "Remember, I like pizza.", "Got it! You like pizza.", store_in_long_term=True
    )

    print(f"Context:\n{context_mgr.get_context_for_agent(include_summary=True)}\n")
    print(f"User name: {context_mgr.get_user_preference('user_name')}")
    print(f"\nFull metrics: {json.dumps(context_mgr.get_full_metrics(), indent=2)}")


if __name__ == "__main__":
    demo()
