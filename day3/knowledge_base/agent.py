# day3/knowledge_base/agent.py - Knowledge base agent with vector storage

from typing import Any, Dict, List, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from common.base.agent import BaseAgent


class KnowledgeBaseAgent(BaseAgent):
    """Agent with long-term memory using vector database."""

    def __init__(self, collection_name: str = "knowledge_base"):
        super().__init__(
            name="KnowledgeBaseAgent",
            description="Agent with semantic search and RAG capabilities"
        )

        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))

        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Knowledge base for agent"}
        )

        self.doc_counter = 0

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Parse input as query or document."""
        text = str(input_data).strip()

        # Determine if it's a query or document to store
        is_query = any(q in text.lower() for q in ['what', 'how', 'why', 'find', 'search'])

        return {
            "text": text,
            "is_query": is_query,
            "length": len(text),
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Decide whether to store or retrieve."""
        return {
            "text": perception["text"],
            "action": "query" if perception["is_query"] else "store",
            "top_k": 3,
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute storage or retrieval."""
        if decision["action"] == "store":
            return self._store_document(decision["text"])
        else:
            return self._query_knowledge(decision["text"], decision["top_k"])

    def _store_document(self, text: str) -> Dict[str, Any]:
        """Store document in vector database."""
        doc_id = f"doc_{self.doc_counter}"
        self.doc_counter += 1

        self.collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[{"source": "user_input"}]
        )

        return {
            "action": "stored",
            "document_id": doc_id,
            "text": text,
        }

    def _query_knowledge(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Query knowledge base with semantic search."""
        results = self.collection.query(
            query_texts=[query],
            n_results=min(top_k, self.collection.count())
        )

        if results['documents'] and results['documents'][0]:
            return {
                "action": "retrieved",
                "query": query,
                "results": [
                    {
                        "text": doc,
                        "id": doc_id,
                        "distance": dist,
                    }
                    for doc, doc_id, dist in zip(
                        results['documents'][0],
                        results['ids'][0],
                        results['distances'][0]
                    )
                ],
                "total_found": len(results['documents'][0]),
            }
        else:
            return {
                "action": "retrieved",
                "query": query,
                "results": [],
                "total_found": 0,
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        return {
            "total_documents": self.collection.count(),
            "collection_name": self.collection.name,
        }


# Demo function
def demo():
    agent = KnowledgeBaseAgent(collection_name="demo_kb")

    # Store some documents
    documents = [
        "Python is a high-level programming language",
        "Machine learning is a subset of artificial intelligence",
        "Neural networks are inspired by biological neurons",
    ]

    print(f"=== {agent.name} Demo ===\n")
    print("Storing documents...")
    for doc in documents:
        result = agent.run(doc)
        print(f"  Stored: {result['document_id']}")

    print(f"\nKnowledge base: {agent.get_stats()}\n")

    # Query
    queries = [
        "What is Python?",
        "Find information about neural networks",
    ]

    print("Querying knowledge base...")
    for query in queries:
        result = agent.run(query)
        print(f"\nQuery: {query}")
        print(f"Found: {result['total_found']} results")
        for i, res in enumerate(result['results'], 1):
            print(f"  {i}. {res['text'][:50]}... (distance: {res['distance']:.3f})")

    print(f"\nMetrics: {agent.get_metrics()}")


if __name__ == "__main__":
    demo()