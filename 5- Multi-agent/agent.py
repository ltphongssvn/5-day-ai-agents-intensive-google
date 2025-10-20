from google.adk.agents import LlmAgent
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

# --- AGENT 1: THE RESEARCHER (WORKER) ---
researcher_agent = LlmAgent(
    name="researcher",
    model="gemini-2.5-flash",
    instruction="""
    You are a researcher. Your only job is to
    use the 'google_search' tool to find information.
    You must return only the raw facts, not a summary.
    """,
    tools=[google_search]
)

# --- AGENT 2: THE WRITER (WORKER) ---
writer_agent = LlmAgent(
    name="writer",
    model="gemini-2.5-flash",
    instruction="""
    You are a professional blog post writer.
    Your only job is to take a set of facts
    and write a short, engaging, 2-paragraph
    blog post based *only* on those facts.
    Do not add any new information.
    """,
    # Note: This agent has NO tools! Its only skill is writing.
)

# --- AGENT 3: THE ORCHESTRATOR (MANAGER) ---
# We turn our worker agents into tools
researcher_tool = AgentTool(researcher_agent)
writer_tool = AgentTool(writer_agent)

root_agent = LlmAgent(
    name="orchestrator",
    model="gemini-2.5-flash",
    instruction="""
    You are the project manager for a research team.
    You have two specialists: 'researcher' and 'writer'.
    
    When the user gives you a topic:
    1.  You MUST first call the 'researcher' tool to get facts.
    2.  You MUST then take the researcher's facts and give
        them to the 'writer' tool to get a blog post.
    3.  You MUST then return the writer's final blog post
        to the user.
    
    Do not do any research or writing yourself. Delegate!
    """,
    # The Orchestrator's tools are the other agents
    tools=[researcher_tool, writer_tool]
)