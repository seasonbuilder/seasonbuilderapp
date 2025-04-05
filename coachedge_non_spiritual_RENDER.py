import os
import openai
import streamlit as st
from translation_non_spiritual import translations  # Ensure this file exists with your translations dictionary
import time

# Initialize the OpenAI client globally
client = openai.OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Coach Edge - Virtual Life Coach",
    layout="wide"
)

# ----------------------------
# Session State Initialization (if not already set)
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
    "processing": False,
    "current_prompt": ""
}
for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ----------------------------
# Initialize OpenAI Assistant and Thread (per session)
# ----------------------------
if st.session_state.assistant is None or st.session_state.thread is None:
    st.session_state.assistant = openai.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))
    st.session_state.thread = client.beta.threads.create()

# ----------------------------
# Retrieve Query Parameters (if any)
# ----------------------------
params = st.query_params
st.session_state.fname = params.get("fname", "Unknown")
st.session_state.school = params.get("school", "Unknown")
st.session_state.team = params.get("team", "Unknown")
st.session_state.role = params.get("role", "Unknown")
st.session_state.language = params.get("language", "English")
st.session_state.prompt = params.get("prompt", "")

# Determine language; default to English if not set
if "(" in st.session_state.language and ")" in st.session_state.language:
    lang = st.session_state.language.split("(")[1].split(")")[0]
else:
    lang = st.session_state.language if st.session_state.language else "English"

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
# Render the Chat Interface: Display prompt instructions and topic buttons
# ----------------------------
st.markdown(lang_translations["ask_question"])
with st.expander(lang_translations["expander_title"]):
    for idx, button_text in enumerate(lang_translations["button_prompts"]):
        if st.button(button_text):
            st.session_state.prompt = lang_translations["prompts"][idx]

# ----------------------------
# Chat Input Container: Only show input when not processing
# ----------------------------
chat_input_container = st.empty()
if st.session_state.processing:
    chat_input_container.info("⏳ Processing your previous request, please wait...")
else:
    user_input = chat_input_container.chat_input(lang_translations["typed_input_placeholder"])
    if user_input:
        st.session_state.prompt = user_input
        st.session_state.processing = True  # Immediately set processing flag
        chat_input_container.empty()  # Hide the input once a prompt is submitted

# ----------------------------
# Display Conversation History
# ----------------------------
for message in st.session_state.messages:
    avatar = (
        "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
        if message["role"] == "user"
        else "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"
    )
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ----------------------------
# Process the Prompt and Stream Assistant Response
# ----------------------------
if st.session_state.processing and st.session_state.prompt:
    # Immediately capture and clear the prompt
    current_prompt = st.session_state.prompt
    st.session_state.prompt = ""
    st.session_state.current_prompt = current_prompt

    # Append the user's prompt to conversation history and display it
    st.session_state.messages.append({"role": "user", "content": current_prompt})
    with st.chat_message("user", avatar="https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"):
        st.markdown(current_prompt)

    with st.chat_message("assistant", avatar="https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"):
        response_container = st.empty()
        # Record the user's message in the thread (this call is specific to your integration)
        st.session_state.thread_messages = client.beta.threads.messages.create(
            st.session_state.thread.id, role="user", content=current_prompt
        )
        # Start streaming the assistant's response from OpenAI
        stream = client.beta.threads.runs.create(
            assistant_id=st.session_state.assistant.id,
            thread_id=st.session_state.thread.id,
            additional_instructions=additional_instructions,
            stream=True
        )
        delta = []
        response_text = ""
        if stream:
            for event in stream:
                if event.data.object == "thread.message.delta":
                    for content in event.data.delta.content:
                        if content.type == "text":
                            delta.append(content.text.value)
                            response_text = "".join(delta).strip()
                            response_container.markdown(response_text)
        # Append the assistant's response to the conversation history
        st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # Reset processing flag and clear temporary prompt
    st.session_state.processing = False
    st.session_state.current_prompt = ""
    st.experimental_rerun()  # Force a rerun to refresh UI and re-display the chat input