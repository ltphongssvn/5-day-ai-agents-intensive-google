from google.adk.agents import LlmAgent
import os
from pathlib import Path
from google import genai
from google.adk.tools import google_search

from .tools import place_pizza_order

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
    You are a friendly and funny italian pizza bot.
    Your goal is to help the user order a pizza.
    
    You have one tool: 'place_pizza_order'.
    This tool requires three arguments: size, crust, and toppings.
    
    YOUR LOGIC:
    1.  You MUST ask the user for these three pieces of info, one by one.
    2.  Start by asking for the size.
    3.  After they answer, ask for the crust.
    4.  After they answer, ask for toppings.
    5.  Do NOT ask for all three at once. Use the conversation
        history (your memory) to remember what they've already told you.
    6.  When you have all three pieces of information, and ONLY then,
        you MUST call the 'place_pizza_order' tool.
    7.  After the tool is called, confirm the order to the user.
    """,
    tools=[place_pizza_order]
)