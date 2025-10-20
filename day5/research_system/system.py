# day5/research_system/system.py - Complete multi-agent research system

from typing import Any, Dict, List
from common.base.agent import BaseAgent
from day2.web_search.agent import WebSearchAgent
from day3.knowledge_base.agent import KnowledgeBaseAgent


class ResearchAgent(BaseAgent):
    """Gathers information from web searches."""

    def __init__(self):
        super().__init__(name="ResearchAgent", description="Data gathering")
        self.search_agent = WebSearchAgent()

    def perceive(self, input_data: Any) -> str:
        return str(input_data)

    def decide(self, perception: str) -> str:
        return perception

    def act(self, decision: str) -> Dict[str, Any]:
        return self.search_agent.run(decision)


class AnalysisAgent(BaseAgent):
    """Analyzes gathered data."""

    def __init__(self):
        super().__init__(name="AnalysisAgent", description="Data analysis")

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        return input_data if isinstance(input_data, dict) else {"data": input_data}

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        return perception

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        results = decision.get("results", [])
        return {
            "summary": f"Analyzed {len(results)} sources",
            "key_findings": [r.get("title", "N/A") for r in results[:3]],
        }


class WriterAgent(BaseAgent):
    """Generates reports."""

    def __init__(self):
        super().__init__(name="WriterAgent", description="Report generation")

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        return input_data if isinstance(input_data, dict) else {"analysis": input_data}

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        return perception

    def act(self, decision: Dict[str, Any]) -> str:
        summary = decision.get("summary", "No summary")
        findings = decision.get("key_findings", [])

        report = f"# Research Report\n\n"
        report += f"## Summary\n{summary}\n\n"
        report += f"## Key Findings\n"
        for i, finding in enumerate(findings, 1):
            report += f"{i}. {finding}\n"

        return report


class QualityAssuranceAgent(BaseAgent):
    """Reviews and validates output."""

    def __init__(self):
        super().__init__(name="QualityAssuranceAgent", description="Quality check")

    def perceive(self, input_data: Any) -> str:
        return str(input_data)

    def decide(self, perception: str) -> Dict[str, Any]:
        return {
            "content": perception,
            "has_summary": "Summary" in perception,
            "has_findings": "Key Findings" in perception,
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        quality_score = 0.0
        if decision["has_summary"]:
            quality_score += 0.5
        if decision["has_findings"]:
            quality_score += 0.5

        return {
            "approved": quality_score >= 0.8,
            "quality_score": quality_score,
            "content": decision["content"],
        }


class ResearchSystem:
    """Multi-agent research system."""

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.writer_agent = WriterAgent()
        self.qa_agent = QualityAssuranceAgent()

    def run_research(self, query: str) -> Dict[str, Any]:
        """Execute full research pipeline."""
        print(f"1. Researching: {query}")
        search_results = self.research_agent.run(query)

        print("2. Analyzing results...")
        analysis = self.analysis_agent.run(search_results)

        print("3. Writing report...")
        report = self.writer_agent.run(analysis)

        print("4. Quality assurance...")
        qa_result = self.qa_agent.run(report)

        return qa_result


# Demo function
def demo():
    system = ResearchSystem()

    queries = [
        "AI agents architecture",
        "Python best practices",
    ]

    print("=== Multi-Agent Research System Demo ===\n")

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        result = system.run_research(query)
        print(f"\nQuality Score: {result['quality_score']:.0%}")
        print(f"Approved: {result['approved']}")
        print(f"\n{result['content']}")
        print("=" * 50)


if __name__ == "__main__":
    demo()