import os
import openai
import streamlit as st
from openai import OpenAI
import uuid
from translation_non_spiritual import translations  # Your translations file

# ----------------------------
# Cache the static OpenAI assistant
# ----------------------------
@st.cache_resource
def get_openai_assistant():
    # Set up the API key (static for all users)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # Retrieve and return the assistant (static object)
    return openai.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))

# Initialize the OpenAI client (no need to cache this if it's lightweight)
client = OpenAI()

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Coach Edge - Virtual Life Coach",
    layout="wide"
)

# ----------------------------
# Session State Initialization (per user)
# ----------------------------
default_state = {
    "messages": [],
    "prompt": "",
    "fname": "",
    "school": "",
    "team": "",
    "role": "",
    "language": "",
    "assistant": None,
    "thread": None,
}
for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ----------------------------
# Initialize Assistant and Thread
# ----------------------------
# Retrieve the static assistant from the cache.
if st.session_state.assistant is None:
    st.session_state.assistant = get_openai_assistant()
# Create a new thread for the user (do not cache this globally)
if st.session_state.thread is None:
    st.session_state.thread = client.beta.threads.create()

# ----------------------------
# Retrieve Query Parameters
# ----------------------------
params = st.query_params
st.session_state.fname = params.get("fname", "Unknown")
st.session_state.school = params.get("school", "Unknown")
st.session_state.team = params.get("team", "Unknown")
st.session_state.role = params.get("role", "Unknown")
st.session_state.language = params.get("language", "Unknown")
st.session_state.prompt = params.get("prompt", "")

# Extract language from parentheses if provided
if "(" in st.session_state.language and ")" in st.session_state.language:
    lang = st.session_state.language.split("(")[1].split(")")[0]
else:
    lang = st.session_state.language or "English"

# ----------------------------
# Additional Instructions for the Assistant
# ----------------------------
additional_instructions = (
    f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of "
    f"{st.session_state.team} at the {st.session_state.school}. Please note that their native language is "
    f"{st.session_state.language}. THIS IS IMPORTANT ... When I ask a question or provide a response, please "
    "respond in their native language regardless of the language they use to ask the question or provide a response. "
    "Pay special attention not to accidentally use words from another language when providing a response."
)

# ----------------------------
# Load Translations from External File
# ----------------------------
lang_translations = translations.get(lang, translations["English"])

# ----------------------------
# Render the Chat Interface
# ----------------------------
st.markdown(lang_translations["ask_question"])

with st.expander(lang_translations["expander_title"]):
    for idx, button_text in enumerate(lang_translations["button_prompts"]):
        if st.button(button_text):
            st.session_state.prompt = lang_translations["prompts"][idx]

typed_input = st.chat_input(lang_translations["typed_input_placeholder"])
if typed_input:
    st.session_state.prompt = typed_input

# Display conversation history
for message in st.session_state.messages:
    avatar = (
        "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
        if message["role"] == "user"
        else "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"
    )
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ----------------------------
# Process New Input and Stream Assistant Response
# ----------------------------
# Initialize the processing flag if not present
if "processing" not in st.session_state:
    st.session_state.processing = False

# Only process new input if no processing is already in progress
if st.session_state.prompt and not st.session_state.processing:
    st.session_state.processing = True  # Mark as processing
    
    # Append the user's prompt to the conversation history
    st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
    with st.chat_message("user", avatar="https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"):
        st.markdown(st.session_state.prompt)
    
    with st.chat_message("assistant", avatar="https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"):
        container = st.empty()
        # Record the user's message in the thread
        st.session_state.thread_messages = client.beta.threads.messages.create(
            st.session_state.thread.id,
            role="user",
            content=st.session_state.prompt
        )
        # Start streaming the assistant's response from OpenAI
        stream = client.beta.threads.runs.create(
            assistant_id=st.session_state.assistant.id,
            thread_id=st.session_state.thread.id,
            additional_instructions=additional_instructions,
            stream=True
        )
        delta = []
        response = ""
        if stream:
            for event in stream:
                if event.data.object == "thread.message.delta":
                    for content in event.data.delta.content:
                        if content.type == "text":
                            delta.append(content.text.value)
                            response = "".join(delta).strip()
                            container.markdown(response)
        # Append the assistant's response to conversation history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear the prompt and mark processing as complete
    st.session_state.prompt = ""
    st.session_state.processing = False