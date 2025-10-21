from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google import genai
import os
from pathlib import Path
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

script_dir = Path(__file__).resolve().parent
dotenv_path = script_dir.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

print(f"Attempting to load .env from: {dotenv_path}")
if not dotenv_path.is_file():
    print("⚠️ WARNING: .env file not found at the specified path.")

ollama_base_url = os.getenv("OLLAMA_API_BASE_URL")
if ollama_base_url:
    print(f"✅ Found OLLAMA_API_BASE_URL: {ollama_base_url}")
else:
    print("⚠️ WARNING: OLLAMA_API_BASE_URL not found in environment.")
    print("LiteLLM will default to localhost. Check your .env file location and content.")
## --- API KEY SETUP for Gemini ---
## Make sure your GEMINI_API_KEY_FILE environment variable is set

# api_key = ""
# try:
#     key_path = Path(os.environ["GEMINI_API_KEY_FILE"])
#     with key_path.open("r", encoding="utf-8") as fh:
#         api_key = fh.read().strip()
# except KeyError:
#     print("Error: GEMINI_API_KEY_FILE environment variable not set.")
#     exit()

# os.environ["GOOGLE_API_KEY"] = api_key
# os.environ["GEMINI_API_KEY"] = api_key
# client = genai.Client(api_key=api_key)
# gemini_model = gemini-2.5-flash

# --- Setup for using Ollama ---
ollama_base_url = os.getenv("OLLAMA_API_BASE_URL")
ollama_model = LiteLlm(model="ollama/granite3-dense:8b",
    api_base=ollama_base_url)

# --- DEFINE CALLBACK FUNCTIONS FIRST ---

def save_user_input_to_state(callback_context: CallbackContext):
    """
    A callback to run before the main sequence.
    It intercepts the user's initial message and saves it
    to the state as 'topic_context' for all other agents to use.
    """
    if callback_context.user_content and callback_context.user_content.parts:
        user_input = callback_context.user_content.parts[0].text
        # Initialize state variables needed for the prompts
        callback_context.session.state["topic_context"] = user_input
        callback_context.session.state["critic_feedback"] = "" # Initialize as empty
        callback_context.session.state["current_draft"] = ""   # Initialize as empty
        print(f"--- Callback: Saved user input to state['topic_context'] ---")
    return None

# --- TOOL TO EXIT LOOP ---
def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the draft is approved and no further revisions are needed."""
    print(f"[Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    return {"status": "Loop exited - draft approved"}


# Define the completion phrase
COMPLETION_PHRASE = "APPROVED"

# --- AGENT 1: THE CRITIC (WORKER) ---
critic_agent = LlmAgent(
    name="critic",
    model=ollama_model,
    instruction=f"""
    You are a podcast critic reviewing a draft.
    
    **Current Draft:**
    {{{{current_draft}}}}
    
    **Original Topic Context:**
    {{{{topic_context}}}}
    
    **Task:**
    Review the draft for:
    - Factual Accuracy (matches topic_context)
    - Engagement
    - Clarity
    - Length (approx 300-330 words)
    - Structure (hook, intro, body, outro)
    
    IF the draft is good and no changes are needed:
    Respond with EXACTLY: "{COMPLETION_PHRASE}" and provide a summary of what you checked and why you approved it.
    
    ELSE:
    Provide specific, actionable feedback for revision.
    
    Output only the critique OR the exact completion phrase.
    """,
    output_key="critic_feedback",
)


# --- AGENT 2: THE WRITER ---
writer_agent = LlmAgent(
    name="WriterAgent",
    model=ollama_model,
    instruction="""
    You are a podcast scriptwriter. write a draft with the following elements in mind:
    - Factual Accuracy (matches topic_context)
    - Engagement
    - Clarity
    - Length (approx 300-330 words)
    - Structure (hook, intro, body, outro)
    
    **IF critic_feedback is empty:**
    Write a brand new 2-minute podcast draft (approx 300-330 words).
    Use the facts from: {topic_context}
    Follow this structure: hook, intro, body, outro.
    
    **IF critic_feedback is present:**
    Revise the current draft based on the feedback.
    
    **Current Draft:**
    {current_draft}
    
    **Critic Feedback:**
    {critic_feedback}
    
    Output only the podcast script text.
    """,
    output_key="current_draft",
    
)

# --- ROOT AGENT: THE PRODUCER ---
root_agent = LoopAgent(
    name="refinement_loop",
    sub_agents=[
        writer_agent,
        critic_agent,
    ],
    max_iterations=3,
    before_agent_callback=save_user_input_to_state
)