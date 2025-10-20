# day6/google_cloud_ml/language_agent.py - Natural Language API Agent for text analysis
import os
from typing import Any, Dict
from google.cloud import language_v1
from common.base.agent import BaseAgent
from common.config.settings import settings


class LanguageAgent(BaseAgent):
    """Agent for text analysis using Google Cloud Natural Language API."""

    def __init__(self):
        super().__init__(
            name="LanguageAgent",
            description="Performs text analysis using Google Cloud Natural Language API",
        )
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_cloud_credentials
        self.client = language_v1.LanguageServiceClient()

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Process text input."""
        return {"text": str(input_data), "type": language_v1.Document.Type.PLAIN_TEXT}

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Create document for analysis."""
        document = language_v1.Document(
            content=perception["text"], type_=perception["type"]
        )
        return {"document": document}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Natural Language API analysis."""
        document = decision["document"]

        # Analyze sentiment
        sentiment = self.client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment

        # Analyze entities
        entities_response = self.client.analyze_entities(request={"document": document})

        # Analyze syntax
        syntax_response = self.client.analyze_syntax(request={"document": document})

        results = {
            "sentiment": {"score": sentiment.score, "magnitude": sentiment.magnitude},
            "entities": [
                {
                    "name": entity.name,
                    "type": language_v1.Entity.Type(entity.type_).name,
                    "salience": entity.salience,
                }
                for entity in entities_response.entities
            ],
            "tokens": [
                {
                    "text": token.text.content,
                    "part_of_speech": language_v1.PartOfSpeech.Tag(
                        token.part_of_speech.tag
                    ).name,
                }
                for token in syntax_response.tokens
            ],
        }

        return results


if __name__ == "__main__":
    print("=== LanguageAgent Demo ===\n")

    agent = LanguageAgent()

    # Test text
    text = "Google Cloud Platform is amazing! It provides powerful AI services."

    print(f"Analyzing: {text}\n")
    result = agent.run(text)

    print(f"Sentiment Score: {result['sentiment']['score']:.2f}")
    print(f"Sentiment Magnitude: {result['sentiment']['magnitude']:.2f}\n")

    print(f"Entities ({len(result['entities'])}):")
    for entity in result["entities"][:5]:
        print(f"  - {entity['name']} ({entity['type']}): {entity['salience']:.2f}")

    print(f"\nMetrics: {agent.get_metrics()}")
