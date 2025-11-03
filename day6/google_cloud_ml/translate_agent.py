# day6/google_cloud_ml/translate_agent.py - Translate API Agent
import os
from typing import Any, Dict, List
from google.cloud import translate_v2 as translate
from common.base.agent import BaseAgent
from common.config.settings import settings


class TranslateAgent(BaseAgent):
    """Agent for translation using Google Cloud Translate API."""

    def __init__(self):
        super().__init__(
            name="TranslateAgent",
            description="Translates text using Google Cloud Translate API",
        )
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_cloud_credentials
        self.client = translate.Client()

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Process translation input."""
        if isinstance(input_data, dict):
            return input_data
        return {"text": str(input_data), "target_language": "en"}

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare translation parameters."""
        return {
            "text": perception["text"],
            "target": perception.get("target_language", "en"),
            "source": perception.get("source_language"),
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute translation."""
        result = self.client.translate(
            decision["text"],
            target_language=decision["target"],
            source_language=decision.get("source"),
        )

        return {
            "translated_text": result["translatedText"],
            "detected_source_language": result.get("detectedSourceLanguage"),
            "input": result["input"],
        }

    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages."""
        return self.client.get_languages()


if __name__ == "__main__":
    print("=== TranslateAgent Demo ===\n")

    agent = TranslateAgent()

    # Test translation
    tests = [
        {"text": "Hello, how are you?", "target_language": "es"},
        {"text": "Bonjour le monde", "target_language": "en"},
        {"text": "こんにちは", "target_language": "en"},
    ]

    for test in tests:
        result = agent.run(test)
        print(f"Input: {result['input']}")
        print(f"Translation: {result['translated_text']}")
        print(f"Detected Language: {result['detected_source_language']}\n")

    print(f"Metrics: {agent.get_metrics()}")
