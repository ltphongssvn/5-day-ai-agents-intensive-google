from google.adk.agents import LlmAgent
import os
from pathlib import Path
from google import genai
from google.adk.tools import google_search

key_path = Path(os.environ["GEMINI_API_KEY_FILE"])
with key_path.open("r", encoding="utf-8") as fh:
    api_key = fh.read().strip()

os.environ["GOOGLE_API_KEY"] = api_key
os.environ["GEMINI_API_KEY"] = api_key

client = genai.Client(api_key=api_key)

# This is the "brain" of our operation.
# We are defining the one and only agent for this project.
root_agent = LlmAgent(
    name="assistant",
    model="gemini-2.5-flash",
    instruction="""
    You are an angry pirate.
    Your name is 'Sparky'.
    When asked who you are, introduce yourself.
    """,
    tools=[google_search]
)