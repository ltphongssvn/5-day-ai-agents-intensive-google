from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools import google_search
# This is the "magic" that lets an agent become a tool
from google.adk.tools import AgentTool
from google import genai
import os
from pathlib import Path

key_path = Path(os.environ["GEMINI_API_KEY_FILE"])
with key_path.open("r", encoding="utf-8") as fh:
    api_key = fh.read().strip()

os.environ["GOOGLE_API_KEY"] = api_key
os.environ["GEMINI_API_KEY"] = api_key

client = genai.Client(api_key=api_key)

# --- AGENT 3: THE ORCHESTRATOR (MANAGER) ---
# We turn our worker agents into tools
root_agent = LlmAgent(
    name="orchestrator",
    model="gemini-2.5-flash",
    instruction="""
    You are a helpful data analyst. You have two tools:
    1. 'google_search': to find current information.
    2. 'BuiltInCodeExecutor': to do math and data processing.
    
    When a user asks a complex question:
    - First, use 'google_search' to find the raw data.
    - Second, use 'BuiltInCodeExecutor' to analyze or calculate
      something based on that data.
    - Finally, give the user the answer.
    """,
    # The Orchestrator's tools are the other agents
    code_executor=BuiltInCodeExecutor(),
    tools=[google_search]
)