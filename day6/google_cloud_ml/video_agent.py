# day6/google_cloud_ml/video_agent.py - Video Intelligence Agent
import os
from typing import Any, Dict
from google.cloud import videointelligence
from common.base.agent import BaseAgent
from common.config.settings import settings


class VideoIntelligenceAgent(BaseAgent):
    """Agent for video analysis using Google Cloud Video Intelligence API."""

    def __init__(self):
        super().__init__(
            name="VideoIntelligenceAgent",
            description="Analyzes videos using Google Cloud Video Intelligence API",
        )
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_cloud_credentials
        self.client = videointelligence.VideoIntelligenceServiceClient()

    def perceive(self, input_data: Any) -> Dict[str, Any]:
        """Process video input - file path or GCS URI."""
        if isinstance(input_data, dict):
            return input_data
        return {
            "uri": str(input_data),
            "features": [
                videointelligence.Feature.LABEL_DETECTION,
                videointelligence.Feature.SHOT_CHANGE_DETECTION,
            ],
        }

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Configure video analysis features."""
        return {"input_uri": perception["uri"], "features": perception["features"]}

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute video analysis."""
        operation = self.client.annotate_video(
            request={
                "input_uri": decision["input_uri"],
                "features": decision["features"],
            }
        )

        print("Processing video... This may take a while.")
        result = operation.result(timeout=300)

        annotation = result.annotation_results[0]

        results = {"labels": [], "shots": []}

        # Extract segment labels
        for label in annotation.segment_label_annotations:
            results["labels"].append(
                {
                    "entity": label.entity.description,
                    "category": (
                        label.category_entities[0].description
                        if label.category_entities
                        else None
                    ),
                    "confidence": (
                        label.segments[0].confidence if label.segments else None
                    ),
                }
            )

        # Extract shot changes
        for shot in annotation.shot_annotations:
            results["shots"].append(
                {
                    "start_time": shot.start_time_offset.seconds,
                    "end_time": shot.end_time_offset.seconds,
                }
            )

        return results


if __name__ == "__main__":
    print("=== VideoIntelligenceAgent Demo ===\n")

    agent = VideoIntelligenceAgent()
    print(f"Agent: {agent.name}")
    print(f"Description: {agent.description}\n")

    print("Ready to analyze videos using Google Cloud Video Intelligence API")
    print("Usage: agent.run('gs://bucket/video.mp4')")
    print("Note: Video must be uploaded to Google Cloud Storage\n")
    print(f"Metrics: {agent.get_metrics()}")
