# day6/google_cloud_ml/vision_agent.py - Vision AI Agent for image recognition
import os
from typing import Any, Dict
from google.cloud import vision
from common.base.agent import BaseAgent
from common.config.settings import settings


class VisionAgent(BaseAgent):
    """Agent for image recognition using Google Cloud Vision API."""

    def __init__(self):
        super().__init__(
            name="VisionAgent",
            description="Performs image analysis using Google Cloud Vision API",
        )
        # Set credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_cloud_credentials
        self.client = vision.ImageAnnotatorClient()

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Process image input - can be file path or image content."""
        if isinstance(input_data, str):
            # File path
            with open(input_data, "rb") as image_file:
                content = image_file.read()
        else:
            # Direct image content
            content = input_data

        return {"content": content, "type": "image"}

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Decide which Vision API features to use."""
        return {
            "content": perception["content"],
            "features": [
                vision.Feature.Type.LABEL_DETECTION,
                vision.Feature.Type.TEXT_DETECTION,
                vision.Feature.Type.FACE_DETECTION,
                vision.Feature.Type.OBJECT_LOCALIZATION,
            ],
        }

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Vision API analysis."""
        image = vision.Image(content=decision["content"])

        # Perform detection
        response = self.client.annotate_image(
            {
                "image": image,
                "features": [{"type_": feature} for feature in decision["features"]],
            }
        )

        results = {"labels": [], "texts": [], "faces": [], "objects": []}

        # Extract labels
        for label in response.label_annotations:
            results["labels"].append(
                {"description": label.description, "score": label.score}
            )

        # Extract text
        for text in response.text_annotations:
            results["texts"].append(
                {
                    "text": text.description,
                    "confidence": getattr(text, "confidence", None),
                }
            )

        # Extract faces
        for face in response.face_annotations:
            results["faces"].append(
                {
                    "joy": face.joy_likelihood.name,
                    "sorrow": face.sorrow_likelihood.name,
                    "anger": face.anger_likelihood.name,
                    "surprise": face.surprise_likelihood.name,
                }
            )

        # Extract objects
        for obj in response.localized_object_annotations:
            results["objects"].append({"name": obj.name, "score": obj.score})

        return results


if __name__ == "__main__":
    print("=== VisionAgent Demo ===\n")

    agent = VisionAgent()
    print(f"Agent: {agent.name}")
    print(f"Description: {agent.description}\n")

    # Note: This requires an actual image file to test
    print("Ready to analyze images using Google Cloud Vision API")
    print("Usage: agent.run('path/to/image.jpg')")
    print(f"\nMetrics: {agent.get_metrics()}")
