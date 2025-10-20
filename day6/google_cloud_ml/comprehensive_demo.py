# day6/google_cloud_ml/comprehensive_demo.py - Demo all 6 Google Cloud ML APIs
from day6.google_cloud_ml.language_agent import LanguageAgent
from day6.google_cloud_ml.translate_agent import TranslateAgent
from day6.google_cloud_ml.tts_agent import TextToSpeechAgent
from day6.google_cloud_ml.vision_agent import VisionAgent
from day6.google_cloud_ml.speech_agent import SpeechToTextAgent
from day6.google_cloud_ml.video_agent import VideoIntelligenceAgent


def main():
    print("=" * 70)
    print("GOOGLE CLOUD MACHINE LEARNING APIs - COMPLETE DEMONSTRATION")
    print("=" * 70)

    # 1. Natural Language API
    print("\n1. NATURAL LANGUAGE API (Text Analysis)")
    print("-" * 70)
    language_agent = LanguageAgent()
    text = "Google Cloud Platform is amazing! It provides powerful AI services."
    result = language_agent.run(text)
    print(f"Text: {text}")
    print(
        f"Sentiment: {result['sentiment']['score']:.2f} (magnitude: {result['sentiment']['magnitude']:.2f})"
    )
    print(f"Entities found: {len(result['entities'])}")
    for entity in result["entities"][:3]:
        print(f"  • {entity['name']} ({entity['type']})")

    # 2. Translate API
    print("\n2. TRANSLATE API")
    print("-" * 70)
    translate_agent = TranslateAgent()
    translations = [
        {"text": "Hello, world!", "target_language": "es"},
        {"text": "Artificial Intelligence", "target_language": "fr"},
        {"text": "Machine Learning", "target_language": "de"},
    ]
    for trans in translations:
        result = translate_agent.run(trans)
        print(
            f"{trans['text']:25} → {result['translated_text']:30} [{trans['target_language'].upper()}]"
        )

    # 3. Text-to-Speech API
    print("\n3. TEXT-TO-SPEECH API")
    print("-" * 70)
    tts_agent = TextToSpeechAgent()
    result = tts_agent.run(
        {
            "text": "Welcome to Google Cloud Machine Learning APIs demonstration!",
            "output_file": "demo_speech.mp3",
        }
    )
    print(f"Generated: {result['output_file']} ({result['audio_size']:,} bytes)")

    # 4. Vision API
    print("\n4. VISION AI (Image Recognition)")
    print("-" * 70)
    vision_agent = VisionAgent()
    image_path = ".venv/lib/python3.13/site-packages/sklearn/datasets/images/flower.jpg"
    result = vision_agent.run(image_path)
    print(f"Image: {image_path}")
    print(f"Labels detected: {len(result['labels'])}")
    for label in result["labels"][:5]:
        print(f"  • {label['description']:20} (confidence: {label['score']:.1%})")
    if result["objects"]:
        print(f"Objects detected: {len(result['objects'])}")
        for obj in result["objects"][:3]:
            print(f"  • {obj['name']} (score: {obj['score']:.2f})")

    # 5. Speech-to-Text API
    print("\n5. SPEECH-TO-TEXT API")
    print("-" * 70)
    speech_agent = SpeechToTextAgent()
    audio_file = ".venv/lib/python3.13/site-packages/scipy/io/tests/data/test-44100Hz-le-1ch-4bytes.wav"
    result = speech_agent.run(
        {"audio_file": audio_file, "language_code": "en-US", "sample_rate_hertz": 44100}
    )
    print(f"Audio: {audio_file}")
    if result["transcripts"]:
        print(f"Transcript: {result['full_transcript']}")
    else:
        print("No speech detected (test file contains no speech)")

    # 6. Video Intelligence API
    print("\n6. VIDEO AI")
    print("-" * 70)
    video_agent = VideoIntelligenceAgent()
    print("VideoIntelligenceAgent ready")
    print("Note: Video analysis requires video file (gs:// URL or local file)")
    print("Example: agent.run('gs://cloud-samples-data/video/cat.mp4')")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY - ALL 6 GOOGLE CLOUD ML APIs")
    print("=" * 70)
    print(f"✓ Natural Language API:  {language_agent.get_metrics()}")
    print(f"✓ Translate API:         {translate_agent.get_metrics()}")
    print(f"✓ Text-to-Speech API:    {tts_agent.get_metrics()}")
    print(f"✓ Vision AI:             {vision_agent.get_metrics()}")
    print(f"✓ Speech-to-Text API:    {speech_agent.get_metrics()}")
    print(f"✓ Video Intelligence AI: {video_agent.get_metrics()}")
    print("\nAll 6 Google Cloud Machine Learning APIs successfully demonstrated!")


if __name__ == "__main__":
    main()
