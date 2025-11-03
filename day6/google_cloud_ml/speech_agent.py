# day6/google_cloud_ml/speech_agent.py - Speech-to-Text Agent
import os
from typing import Any, Dict
from google.cloud import speech
from common.base.agent import BaseAgent
from common.config.settings import settings


class SpeechToTextAgent(BaseAgent):
    """Agent for speech recognition using Google Cloud Speech-to-Text API."""

    def __init__(self):
        super().__init__(
            name="SpeechToTextAgent",
            description="Converts speech to text using Google Cloud Speech-to-Text API",
        )
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_cloud_credentials
        self.client = speech.SpeechClient()

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Process audio input - file path, dict with audio_file, or audio content."""
        # Handle dictionary input
        if isinstance(input_data, dict):
            audio_file = input_data.get("audio_file")
            with open(audio_file, "rb") as f:
                content = f.read()
            language = input_data.get("language_code", "en-US")
            sample_rate = input_data.get("sample_rate_hertz", 16000)
        # Handle string path
        elif isinstance(input_data, str):
            with open(input_data, "rb") as audio_file:
                content = audio_file.read()
            language = "en-US"
            sample_rate = 16000
        # Handle raw bytes
        else:
            content = input_data
            language = "en-US"
            sample_rate = 16000

        return {
            "content": content,
            "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
            "sample_rate": sample_rate,
            "language": language,
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Configure recognition settings."""
        config = speech.RecognitionConfig(
            encoding=perception["encoding"],
            sample_rate_hertz=perception["sample_rate"],
            language_code=perception["language"],
            enable_automatic_punctuation=True,
        )

        audio = speech.RecognitionAudio(content=perception["content"])

        return {"config": config, "audio": audio}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute speech recognition."""
        response = self.client.recognize(
            config=decision["config"], audio=decision["audio"]
        )

        results = []
        for result in response.results:
            alternative = result.alternatives[0]
            results.append(
                {
                    "transcript": alternative.transcript,
                    "confidence": alternative.confidence,
                }
            )

        return {
            "transcripts": results,
            "full_transcript": " ".join([r["transcript"] for r in results]),
        }


if __name__ == "__main__":
    print("=== SpeechToTextAgent Demo ===\n")
    agent = SpeechToTextAgent()
    print(f"Agent: {agent.name}")
    print(f"Description: {agent.description}\n")
    print("Ready to transcribe audio using Google Cloud Speech-to-Text API")
    print("Usage: agent.run('path/to/audio.wav')")
    print(f"\nMetrics: {agent.get_metrics()}")
