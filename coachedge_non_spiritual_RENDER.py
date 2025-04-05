import os
import openai
import streamlit as st
from openai import OpenAI
from translation_non_spiritual import translations  # Ensure this file exists and defines your translations

# Initialize OpenAI client globally
client = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Coach Edge - Virtual Life Coach",
    layout="wide"
)

# ----------------------------
# Session State Initialization
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
    "waiting_for_response": False,
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
# Retrieve Query Parameters (once)
# ----------------------------
params = st.query_params
st.session_state.fname = params.get("fname", "Unknown")
st.session_state.school = params.get("school", "Unknown")
st.session_state.team = params.get("team", "Unknown")
st.session_state.role = params.get("role", "Unknown")
st.session_state.language = params.get("language", "Unknown")
# Also load any pre-set prompt from URL if provided
st.session_state.prompt = params.get("prompt", "")

# Determine language (if provided with parentheses, extract inner value; otherwise default to "English")
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
    f"{st.session_state.language}. When I ask a question, please respond in their native language."
)

# ----------------------------
# Load Translations from External File
# ----------------------------
lang_translations = translations.get(lang, translations["English"])

# ----------------------------
# Render Conversation History
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
# Chat Input (disabled if waiting for response)
# ----------------------------
# Use a container for the chat input so we can hide it when processing
chat_input_container = st.empty()

if st.session_state.waiting_for_response:
    # If waiting, display a message and disable input
    _ = chat_input_container.chat_input(lang_translations["typed_input_placeholder"], disabled=True)
    st.info("Coach Edge is processing your previous response. Please wait...")
else:
    # If not waiting, allow user input
    st.markdown(lang_translations["ask_question"])

    with st.expander(lang_translations["expander_title"]):
        for idx, button_text in enumerate(lang_translations["button_prompts"]):
            if st.button(button_text):
                st.session_state.prompt = lang_translations["prompts"][idx]

    prompt = chat_input_container.chat_input(lang_translations["typed_input_placeholder"], disabled=False)
    # If user submits a prompt and we are not waiting
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.waiting_for_response = True
        st.rerun()  # Rerun to process the prompt

# ----------------------------
# Process the Prompt and Stream Assistant Response
# ----------------------------
# If waiting is True (i.e. a prompt has been submitted) and the last message is from the user, process it.
if st.session_state.waiting_for_response and st.session_state.messages:
    last_message = st.session_state.messages[-1]
    if last_message["role"] == "user":
        with st.chat_message("assistant", avatar="https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"):
            response_container = st.empty()
            # Record the user's message in the thread
            client.beta.threads.messages.create(
                st.session_state.thread.id, role="user", content=last_message["content"]
            )
            # Start streaming the assistant's response
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
            st.session_state.messages.append({"role": "assistant", "content": response_text})
    # After processing, clear the waiting flag and rerun
    st.session_state.waiting_for_response = False
    st.rerun()