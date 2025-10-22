# day2/web_search/agent.py - Web search agent with API integration

from typing import Any, Dict, List, Optional
import requests
from common.base.agent import BaseAgent


class WebSearchAgent(BaseAgent):
    """Agent that performs web searches and parses results."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="WebSearchAgent",
            description="Agent with web search capabilities"
        )
        self.api_key = api_key
        self.search_history: List[Dict[str, Any]] = []

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Extract search query from input."""
        query = str(input_data).strip()
        return {
            "query": query,
            "query_length": len(query),
            "has_quotes": '"' in query,
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Determine search strategy."""
        query = perception["query"]

        decision = {
            "search_query": query,
            "max_results": 5,
            "use_mock": not self.api_key,  # Use mock if no API key
        }

        return decision

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute search and return results."""
        if decision["use_mock"]:
            # Mock search results for demo
            results = self._mock_search(decision["search_query"])
        else:
            # Real API search (placeholder for actual implementation)
            results = self._api_search(decision["search_query"])

        # Store in history
        self.search_history.append({
            "query": decision["search_query"],
            "results_count": len(results),
        })

        return {
            "query": decision["search_query"],
            "results": results,
            "total_found": len(results),
        }

    def _mock_search(self, query: str) -> List[Dict[str, str]]:
        """Generate mock search results for demo."""
        return [
            {
                "title": f"Result 1 for '{query}'",
                "url": f"https://example.com/result1?q={query.replace(' ', '+')}",
                "snippet": f"This is a mock search result about {query}...",
            },
            {
                "title": f"Result 2 for '{query}'",
                "url": f"https://example.com/result2?q={query.replace(' ', '+')}",
                "snippet": f"Another relevant result discussing {query}...",
            },
            {
                "title": f"Result 3 for '{query}'",
                "url": f"https://example.com/result3?q={query.replace(' ', '+')}",
                "snippet": f"Additional information about {query}...",
            },
        ]

    def _api_search(self, query: str) -> List[Dict[str, str]]:
        """Perform actual API search (placeholder)."""
        # This would integrate with real search API (Google, Bing, etc.)
        # For now, return mock data
        return self._mock_search(query)

    def get_search_history(self) -> List[Dict[str, Any]]:
        """Return search history."""
        return self.search_history.copy()


# Demo function
def demo():
    agent = WebSearchAgent()

    test_queries = [
        "Python programming",
        "AI agents architecture",
        "weather forecast",
    ]

    print(f"=== {agent.name} Demo ===\n")
    for query in test_queries:
        result = agent.run(query)
        print(f"Query: {result['query']}")
        print(f"Found: {result['total_found']} results")
        for i, res in enumerate(result['results'], 1):
            print(f"  {i}. {res['title']}")
            print(f"     {res['url']}")
        print()

    print(f"Search History: {len(agent.get_search_history())} queries")
    print(f"Metrics: {agent.get_metrics()}")


if __name__ == "__main__":
    demo()