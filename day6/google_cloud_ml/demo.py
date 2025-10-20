# day6/google_cloud_ml/demo.py - Comprehensive demo of all Google Cloud ML API agents
from day6.google_cloud_ml.language_agent import LanguageAgent
from day6.google_cloud_ml.translate_agent import TranslateAgent
from day6.google_cloud_ml.tts_agent import TextToSpeechAgent


def main():
    print("=" * 60)
    print("Google Cloud ML APIs - Comprehensive Demo")
    print("=" * 60)

    # 1. Natural Language API Demo
    print("\n1. NATURAL LANGUAGE API")
    print("-" * 60)
    language_agent = LanguageAgent()
    text = "Google Cloud Platform is amazing! It provides powerful AI services."
    result = language_agent.run(text)
    print(f"Text: {text}")
    print(
        f"Sentiment: {result['sentiment']['score']:.2f} (magnitude: {result['sentiment']['magnitude']:.2f})"
    )
    print(f"Entities: {len(result['entities'])}")
    for entity in result["entities"][:3]:
        print(f"  - {entity['name']} ({entity['type']})")

    # 2. Translate API Demo
    print("\n2. TRANSLATE API")
    print("-" * 60)
    translate_agent = TranslateAgent()
    translations = [
        {"text": "Hello, world!", "target_language": "es"},
        {"text": "How are you?", "target_language": "fr"},
    ]
    for trans in translations:
        result = translate_agent.run(trans)
        print(
            f"{result['input']} → {result['translated_text']} ({result['detected_source_language']})"
        )

    # 3. Text-to-Speech API Demo
    print("\n3. TEXT-TO-SPEECH API")
    print("-" * 60)
    tts_agent = TextToSpeechAgent()
    result = tts_agent.run(
        {
            "text": "Welcome to Google Cloud Machine Learning APIs!",
            "output_file": "welcome.mp3",
        }
    )
    print(f"Generated: {result['output_file']} ({result['audio_size']} bytes)")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Natural Language: {language_agent.get_metrics()}")
    print(f"Translate: {translate_agent.get_metrics()}")
    print(f"Text-to-Speech: {tts_agent.get_metrics()}")
    print("\nNote: Vision, Video, and Speech-to-Text require media files")


if __name__ == "__main__":
    main()
