# import os
# import openai
# import streamlit as st
# from openai import OpenAI
# from translations_spiritual import translations

# # Constants for avatar URLs
# USER_AVATAR = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
# ASSISTANT_AVATAR = "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"

# # Initialize OpenAI client
# client = OpenAI()

# # Set page configuration
# st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# # Initialize session state with defaults.
# defaults = {
#     "messages": [],
#     "prompt": "",             # Not used for storing submitted text.
#     "submitted_prompt": "",   # This will hold the user's submitted prompt.
#     "fname": "",
#     "school": "",
#     "team": "",
#     "role": "",
#     "language": "",
#     "processing": False,      # When True, chat_input is disabled.
# }
# for key, default in defaults.items():
#     st.session_state.setdefault(key, default)

# def initialize_openai_assistant():
#     """Initialize the OpenAI assistant and thread if not already set."""
#     if "assistant" not in st.session_state or "thread" not in st.session_state:
#         openai.api_key = os.getenv("OPENAI_API_KEY")
#         st.session_state.assistant = openai.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))
#         st.session_state.thread = client.beta.threads.create()

# def get_url_parameters():
#     """Retrieve URL parameters and update session state."""
#     params = st.query_params
#     st.session_state.fname = params.get("fname", "Unknown")
#     st.session_state.school = params.get("school", "Unknown")
#     st.session_state.team = params.get("team", "Unknown")
#     st.session_state.role = params.get("role", "Unknown")
#     st.session_state.language = params.get("language", "Unknown")
#     # Optionally, set an initial prompt from URL params.
#     st.session_state.prompt = params.get("prompt", "")

# def extract_language(lang_str):
#     """Extract language from a string formatted as '... (Language)'."""
#     parts = lang_str.split('(')
#     if len(parts) > 1:
#         return parts[1].split(')')[0]
#     return "Unknown"

# def display_chat_messages():
#     """Display all chat messages stored in session state."""
#     for message in st.session_state.messages:
#         role = message["role"]
#         avatar = USER_AVATAR if role == "user" else ASSISTANT_AVATAR
#         with st.chat_message(role, avatar=avatar):
#             st.markdown(message["content"])

# def process_user_prompt(prompt, additional_instructions):
#     """Send the user prompt to the assistant and stream the response."""
#     # Append and display the user's message.
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user", avatar=USER_AVATAR):
#         st.markdown(prompt)

#     # Send the user's prompt to the thread.
#     st.session_state.thread_messages = client.beta.threads.messages.create(
#         st.session_state.thread.id, role="user", content=prompt
#     )

#     response_chunks = []
#     with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
#         container = st.empty()
#         stream = client.beta.threads.runs.create(
#             assistant_id=st.session_state.assistant.id,
#             thread_id=st.session_state.thread.id,
#             additional_instructions=additional_instructions,
#             stream=True
#         )
#         if stream:
#             for event in stream:
#                 if event.data.object == "thread.message.delta":
#                     for content in event.data.delta.content:
#                         if content.type == "text":
#                             response_chunks.append(content.text.value)
#                             current_response = "".join(response_chunks).strip()
#                             container.markdown(current_response)

#     final_response = "".join(response_chunks).strip()
#     st.session_state.messages.append({"role": "assistant", "content": final_response})
    
#     # Clear the submitted prompt and re-enable chat input.
#     st.session_state.submitted_prompt = ""
#     st.session_state.processing = False
#     st.rerun()  # Force a UI refresh so the chat input is re-enabled.

# def chat_submit_callback():
#     """Callback invoked on chat input submission.
#     It copies the chat input value into 'submitted_prompt' and disables further input.
#     """
#     st.session_state.submitted_prompt = st.session_state.user_input
#     st.session_state.processing = True

# # Main execution flow
# initialize_openai_assistant()
# get_url_parameters()

# # Get language translations.
# lang = extract_language(st.session_state.language)
# lang_translations = translations.get(lang, translations["English"])

# st.markdown(lang_translations["ask_question"])

# # Display preset prompt buttons inside an expander.
# with st.expander(lang_translations["expander_title"]):
#     for idx, button_text in enumerate(lang_translations["button_prompts"]):
#         if st.button(button_text):
#             st.session_state.submitted_prompt = lang_translations["prompts"][idx]
#             st.session_state.processing = True

# # Display existing chat messages.
# display_chat_messages()

# # Render the chat input widget.
# if st.session_state.processing:
#     st.chat_input(lang_translations["typed_input_placeholder"], disabled=True)
# else:
#     _ = st.chat_input(
#         lang_translations["typed_input_placeholder"],
#         key="user_input",
#         on_submit=chat_submit_callback
#     )

# # Process the prompt if set.
# if st.session_state.submitted_prompt and st.session_state.processing:
#     additional_instructions = (
#         f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of "
#         f"{st.session_state.team} at the {st.session_state.school}. Please note that their native language is "
#         f"{st.session_state.language}. THIS IS IMPORTANT ... When I ask a question or provide a response, please "
#         f"respond in their native language regardless of the language they use to ask the question or provide a response. "
#         "Pay special attention not to accidentally use words from another language when providing a response."
#     )
#     process_user_prompt(st.session_state.submitted_prompt, additional_instructions)

import openai
import os
import requests
import streamlit as st
from openai import OpenAI
from translations_spiritual import translations

# Constants for avatar URLs
USER_AVATAR = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
ASSISTANT_AVATAR = "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"

# Initialize OpenAI client
client = OpenAI()

# Set page configuration
st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# Initialize session state with defaults.
defaults = {
    "messages": [],
    "prompt": "",             # Not used for storing submitted text.
    "submitted_prompt": "",   # This will hold the user's submitted prompt.
    "fname": "",
    "school": "",
    "team": "",
    "role": "",
    "language": "",
    "processing": False,      # When True, chat_input is disabled.
    "thread": None,           # Will store the OpenAI conversation thread.
    "assistant": None,        # The OpenAI assistant.
}
for key, default in defaults.items():
    st.session_state.setdefault(key, default)

# -----------------------------
# Adalo Integration Functions
# -----------------------------
def update_adalo_user_thread(email, thread_id):
    """
    Look up the Adalo user record by email and update its thread_id.
    """
    # Retrieve secrets from st.secrets
    ADALO_APP_ID = os.getenv("APP_ID")
    ADALO_COLLECTION_ID = os.getenv("ADALO_COLLECTION_ID")
    ADALO_API_KEY = os.getenv("ADALO_API_KEY")
    headers = {
        "Authorization": f"Bearer {ADALO_API_KEY}",
        "Content-Type": "application/json"
    }
    # URL to get user records filtered by email.
    get_url = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}?filterKey=Email&filterValue={email}"
    response = requests.get(get_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("records") and len(data["records"]) > 0:
            # Assume the first record is the correct one.
            record = data["records"][0]
            element_id = record.get("id")  # Adjust this if your field name is different.
            update_url = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}/{element_id}"
            # st.write("DEBUG:", update_url)
            # st.write("DEBUG:", headers)
            payload = {"thread_id": thread_id}
            update_response = requests.put(update_url, json=payload, headers=headers)
            if update_response.status_code == 200:
                #st.write("DEBUG: Successfully updated Adalo user record with thread_id.")
            else:
                st.write("DEBUG: Failed to update Adalo record:", update_response.text)
        else:
            st.write("DEBUG: No Adalo record found for email:", email)
    else:
        st.write("DEBUG: Failed to retrieve Adalo records:", response.text)

# -----------------------------
# OpenAI Thread Handling
# -----------------------------
def initialize_openai_assistant():
    """Initialize the OpenAI assistant if not already set."""
    if not st.session_state.assistant:
        # Use secrets for API keys.
        openai.api_key = os.getenv("OPENAI_API_KEY")
        st.session_state.assistant = openai.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))

def handle_thread():
    """
    Handle the OpenAI thread. If a thread_id is provided via URL parameters, retrieve that thread.
    Otherwise, create a new thread, update the Adalo user record, and use the new thread.
    """
    params = st.query_params
    if "thread_id" in params and params["thread_id"]:
        thread_id = params["thread_id"]
        st.session_state.thread = openai.beta.threads.retrieve(thread_id)
       # st.write("DEBUG: Retrieved thread with id:", thread_id)
    else:
        # Create a new thread.
        new_thread = client.beta.threads.create()
        st.session_state.thread = new_thread
       # st.write("DEBUG: Created new thread with id:", new_thread.id)
        # Update the Adalo user record with the new thread id.
        email = params.get("email", "")
        if email:
            update_adalo_user_thread(email, new_thread.id)
        else:
            st.write("DEBUG: No email provided; cannot update Adalo record.")

def get_url_parameters():
    """Retrieve URL parameters and update session state."""
    params = st.query_params
    st.session_state.fname = params.get("fname", "Unknown")
    st.session_state.school = params.get("school", "Unknown")
    st.session_state.team = params.get("team", "Unknown")
    st.session_state.role = params.get("role", "Unknown")
    st.session_state.language = params.get("language", "Unknown")
    # Also capture an optional prompt.
    st.session_state.prompt = params.get("prompt", "")

def extract_language(lang_str):
    """Extract language from a string formatted as '... (Language)'."""
    parts = lang_str.split('(')
    if len(parts) > 1:
        return parts[1].split(')')[0]
    return "Unknown"

# -----------------------------
# Chat and Message Functions
# -----------------------------
def display_chat_messages():
    """Display all chat messages stored in session state."""
    for message in st.session_state.messages:
        role = message["role"]
        avatar = USER_AVATAR if role == "user" else ASSISTANT_AVATAR
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

def process_user_prompt(prompt, additional_instructions):
    """Send the user prompt to the assistant and stream the response."""
    # Append and display the user's message.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Send the user's prompt to the thread.
    st.session_state.thread_messages = client.beta.threads.messages.create(
        st.session_state.thread.id, role="user", content=prompt
    )

    response_chunks = []
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        container = st.empty()
        stream = client.beta.threads.runs.create(
            assistant_id=st.session_state.assistant.id,
            thread_id=st.session_state.thread.id,
            additional_instructions=additional_instructions,
            stream=True
        )
        if stream:
            for event in stream:
                if event.data.object == "thread.message.delta":
                    for content in event.data.delta.content:
                        if content.type == "text":
                            response_chunks.append(content.text.value)
                            current_response = "".join(response_chunks).strip()
                            container.markdown(current_response)

    final_response = "".join(response_chunks).strip()
    st.session_state.messages.append({"role": "assistant", "content": final_response})
    
    # Clear the submitted prompt and re-enable chat input.
    st.session_state.submitted_prompt = ""
    st.session_state.processing = False
    st.rerun()  # Force a UI refresh so the chat input is re-enabled.

def chat_submit_callback():
    """Callback invoked on chat input submission.
    It copies the chat input value into 'submitted_prompt' and disables further input.
    """
    st.session_state.submitted_prompt = st.session_state.user_input
    st.session_state.processing = True

# -----------------------------
# Main Execution Flow
# -----------------------------
initialize_openai_assistant()
get_url_parameters()
handle_thread()  # Use URL thread_id if available; otherwise, create a new one and update Adalo.

# Get language translations.
lang = extract_language(st.session_state.language)
lang_translations = translations.get(lang, translations["English"])

st.markdown(lang_translations["ask_question"])

# Display preset prompt buttons inside an expander.
with st.expander(lang_translations["expander_title"]):
    for idx, button_text in enumerate(lang_translations["button_prompts"]):
        if st.button(button_text):
            st.session_state.submitted_prompt = lang_translations["prompts"][idx]
            st.session_state.processing = True

# Display existing chat messages.
display_chat_messages()

# Render the chat input widget.
if st.session_state.processing:
    st.chat_input(lang_translations["typed_input_placeholder"], disabled=True)
else:
    _ = st.chat_input(
        lang_translations["typed_input_placeholder"],
        key="user_input",
        on_submit=chat_submit_callback
    )

# Process the prompt if set.
if st.session_state.submitted_prompt and st.session_state.processing:
    additional_instructions = (
        f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of "
        f"{st.session_state.team} at the {st.session_state.school}. Please note that their native language is "
        f"{st.session_state.language}. THIS IS IMPORTANT ... When I ask a question or provide a response, please "
        f"respond in their native language regardless of the language they use to ask the question or provide a response. "
        f"Pay special attention not to accidentally use words from another language when providing a response."
    )
    process_user_prompt(st.session_state.submitted_prompt, additional_instructions)