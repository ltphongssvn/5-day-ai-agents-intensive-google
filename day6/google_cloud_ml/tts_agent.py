# day6/google_cloud_ml/tts_agent.py - Text-to-Speech Agent
import os
from typing import Any, Dict
from google.cloud import texttospeech
from common.base.agent import BaseAgent
from common.config.settings import settings


class TextToSpeechAgent(BaseAgent):
    """Agent for text-to-speech conversion using Google Cloud Text-to-Speech API."""

    def __init__(self):
        super().__init__(
            name="TextToSpeechAgent",
            description="Converts text to speech using Google Cloud Text-to-Speech API",
        )
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_cloud_credentials
        self.client = texttospeech.TextToSpeechClient()

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Process text input."""
        if isinstance(input_data, dict):
            return {
                "text": input_data.get("text", ""),
                "language": input_data.get("language", "en-US"),
                "voice_name": input_data.get("voice_name", "en-US-Neural2-C"),
                "output_file": input_data.get("output_file", "output.mp3"),
            }
        return {
            "text": str(input_data),
            "language": "en-US",
            "voice_name": "en-US-Neural2-C",
            "output_file": "output.mp3",
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Configure synthesis settings."""
        synthesis_input = texttospeech.SynthesisInput(text=perception["text"])

        voice = texttospeech.VoiceSelectionParams(
            language_code=perception["language"],
            name=perception.get("voice_name"),
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        return {
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
            "output_file": perception["output_file"],
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute text-to-speech synthesis."""
        response = self.client.synthesize_speech(
            input=decision["input"],
            voice=decision["voice"],
            audio_config=decision["audio_config"],
        )

        # Save audio to file
        output_file = decision["output_file"]
        with open(output_file, "wb") as out:
            out.write(response.audio_content)

        return {
            "output_file": output_file,
            "audio_size": len(response.audio_content),
            "success": True,
        }


if __name__ == "__main__":
    print("=== TextToSpeechAgent Demo ===\n")

    agent = TextToSpeechAgent()

    # Test synthesis
    test_text = "Hello! This is a test of Google Cloud Text-to-Speech API."

    result = agent.run({"text": test_text, "output_file": "test_output.mp3"})

    print(f"Text: {test_text}")
    print(f"Output: {result['output_file']}")
    print(f"Size: {result['audio_size']} bytes")
    print(f"\nMetrics: {agent.get_metrics()}")
