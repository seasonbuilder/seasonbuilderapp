import os
import streamlit as st
import openai
from openai import OpenAI
from translation_non_spiritual import translations

# Initialize OpenAI client globally
client = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "assistant" not in st.session_state:
    st.session_state.assistant = openai.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))
if "thread" not in st.session_state:
    st.session_state.thread = client.beta.threads.create()

# Retrieve URL parameters once
params = st.query_params
fname = params.get("fname", "Unknown")
school = params.get("school", "Unknown")
team = params.get("team", "Unknown")
role = params.get("role", "Unknown")
language = params.get("language", "English")
prompt_param = params.get("prompt", "")

# Get language translations
lang = language.split("(")[-1].replace(")", "") if "(" in language else language
lang_translations = translations.get(lang, translations["English"])

# Display UI
st.markdown(lang_translations["ask_question"])
with st.expander(lang_translations["expander_title"]):
    for idx, button_text in enumerate(lang_translations["button_prompts"]):
        if st.button(button_text, disabled=st.session_state.processing):
            st.session_state.prompt = lang_translations["prompts"][idx]

# Chat Input Container (conditionally displayed)
chat_input_container = st.empty()

# Only show input if not processing
if not st.session_state.processing:
    user_input = chat_input_container.chat_input(lang_translations["typed_input_placeholder"])
    if user_input:
        st.session_state.prompt = user_input
        st.session_state.processing = True  # Set processing flag immediately
else:
    chat_input_container.info("⏳ Please wait while Coach Edge responds...")

# Display chat history (always)
for message in st.session_state.messages:
    avatar_url = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png" if message["role"] == "user" else "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"
    with st.chat_message(message["role"], avatar=avatar_url):
        st.markdown(message["content"])

# If there's a prompt and we are in processing mode, process it
if st.session_state.processing and "prompt" in st.session_state:
    current_prompt = st.session_state.prompt
    del st.session_state.prompt  # Clear immediately to avoid conflicts

    # Display user's prompt immediately
    st.session_state.messages.append({"role": "user", "content": current_prompt})
    with st.chat_message("user", avatar="https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"):
        st.markdown(current_prompt)

    # Display assistant avatar immediately
    with st.chat_message("assistant", avatar="https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"):
        response_placeholder = st.empty()

        # Create message in thread
        client.beta.threads.messages.create(
            st.session_state.thread.id, role="user", content=current_prompt
        )

        # Stream the response
        stream = client.beta.threads.runs.create(
            assistant_id=st.session_state.assistant.id,
            thread_id=st.session_state.thread.id,
            additional_instructions=f"User's name: {fname}. They are a {role} in {team} at {school}. Respond in their native language ({language}).",
            stream=True
        )

        full_response = ""
        for event in stream:
            if event.data.object == "thread.message.delta":
                for content in event.data.delta.content:
                    if content.type == "text":
                        full_response += content.text.value
                        response_placeholder.markdown(full_response)

        # Save final response
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.session_state.processing = False  # Reset flag once complete
    st.rerun()  # Force a clean rerun to refresh UI immediately after response completion