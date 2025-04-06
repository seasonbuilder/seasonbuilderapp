# import openai
# import os
# import streamlit as st
# from openai import OpenAI
# import uuid
# from translation_non_spiritual import translations 

# client = OpenAI()

# st.set_page_config(page_title="Coach Edge - Virtual Life Coach",layout="wide")

# #Initialize session state variables

# if "messages" not in st.session_state:
#    st.session_state.messages = []

# if 'prompt' not in st.session_state:
#    st.session_state.prompt = ''

# if 'fname' not in st.session_state:
#     st.session_state.fname = ''  

# if 'school' not in st.session_state:
#     st.session_state.school = ''  

# if 'team' not in st.session_state:
#     st.session_state.team = ''  

# if 'role' not in st.session_state:
#     st.session_state.role = ''  

# if 'language' not in st.session_state:
#     st.session_state.language = ''  

# # Initialize OpenAI assistant and thread
# if "assistant" not in st.session_state or "thread" not in st.session_state:
#     openai.api_key = os.getenv("OPENAI_API_KEY")
#     st.session_state.assistant = openai.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))
#     st.session_state.thread = client.beta.threads.create()

# # Retrieve URL Parameters
# st.session_state.fname = st.query_params.get("fname", "Unknown")
# st.session_state.school = st.query_params.get("school", "Unknown")
# st.session_state.team = st.query_params.get("team", "Unknown")
# st.session_state.role = st.query_params.get("role", "Unknown")
# st.session_state.language = st.query_params.get("language", "Unknown")
# st.session_state.prompt=st.query_params.get("prompt")

# # Extract language from parentheses
# parts = st.session_state.language.split('(')
# if len(parts) > 1:
#     lang = parts[1].split(')')[0]
# else:
#     lang = "Unknown"

# additional_instructions = f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of {st.session_state.team} at the {st.session_state.school}.  Please note that their native language is {st.session_state.language}. THIS IS IMPORTANT ... When I ask a question or provide a response, please respond in their native language regardless of the language they use to ask the question or they provide a response. Pay special attention not to accidentally use words from another language when providing a response."


# # Get the translations for the selected language, default to English
# lang_translations = translations.get(lang, translations["English"])

# st.markdown(lang_translations["ask_question"])

# with st.expander(lang_translations["expander_title"]):
#     for idx, button_text in enumerate(lang_translations["button_prompts"]):
#         if st.button(button_text):
#             st.session_state.prompt = lang_translations["prompts"][idx]

# typed_input = st.chat_input(lang_translations["typed_input_placeholder"])

# # Check if there is typed input
# if typed_input:
#     st.session_state.prompt = typed_input

# for message in st.session_state.messages:
#     if message["role"] == "user":
#        with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#           st.markdown(message["content"])
#     else:
#        with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#           st.markdown(message["content"])

# if st.session_state.prompt:
#     delta = [] 
#     response = ""
#     st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
#     with st.chat_message('user',avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#         st.markdown(st.session_state.prompt)
#     with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#         container = st.empty()
#         st.session_state.thread_messages= client.beta.threads.messages.create(
#               st.session_state.thread.id, role="user",content=st.session_state.prompt
#         )

#         stream = client.beta.threads.runs.create(
#             assistant_id=st.session_state.assistant.id,
#             thread_id = st.session_state.thread.id,
#             additional_instructions = additional_instructions,
#             stream = True
#         )
#         if stream:
#            for event in stream:
#               if event.data.object == "thread.message.delta":
#                  for content in event.data.delta.content:
#                     if content.type == 'text':
#                        delta.append(content.text.value)
#                        response = "".join(item for item in delta if item).strip()
#                        container.markdown(response)
#     st.session_state.messages.append({"role": "assistant", "content": response}) 
#                                                           
import os
import openai
import streamlit as st
from openai import OpenAI
from translation_non_spiritual import translations

# Constants for avatar URLs
USER_AVATAR = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
ASSISTANT_AVATAR = "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"

# Initialize OpenAI client
client = OpenAI()

# Set page configuration
st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# Initialize session state with defaults
defaults = {
    "messages": [],
    "prompt": "",
    "fname": "",
    "school": "",
    "team": "",
    "role": "",
    "language": "",
    "processing": False,  # Flag to control chat input state
}
for key, default in defaults.items():
    st.session_state.setdefault(key, default)


def initialize_openai_assistant():
    """Initialize the OpenAI assistant and thread if not already set."""
    if "assistant" not in st.session_state or "thread" not in st.session_state:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        st.session_state.assistant = openai.beta.assistants.retrieve(
            os.getenv("OPENAI_ASSISTANT")
        )
        st.session_state.thread = client.beta.threads.create()


def get_url_parameters():
    """Retrieve URL parameters and update session state."""
    params = st.query_params
    st.session_state.fname = params.get("fname", "Unknown")
    st.session_state.school = params.get("school", "Unknown")
    st.session_state.team = params.get("team", "Unknown")
    st.session_state.role = params.get("role", "Unknown")
    st.session_state.language = params.get("language", "Unknown")
    st.session_state.prompt = params.get("prompt", "")


def extract_language(lang_str):
    """Extract language from a string formatted as '... (Language)'."""
    parts = lang_str.split('(')
    if len(parts) > 1:
        return parts[1].split(')')[0]
    return "Unknown"


def display_chat_messages():
    """Display all chat messages stored in session state."""
    for message in st.session_state.messages:
        role = message["role"]
        avatar = USER_AVATAR if role == "user" else ASSISTANT_AVATAR
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])


def process_user_prompt(prompt, additional_instructions):
    """Send the user prompt to the assistant and stream the response."""
    # Append and display the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Send the user prompt to the thread
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
    
    # Reset processing flag and clear prompt to allow new input
    st.session_state.processing = False
    st.session_state.prompt = ""


# Main execution flow
initialize_openai_assistant()
get_url_parameters()

# Get language translations
lang = extract_language(st.session_state.language)
lang_translations = translations.get(lang, translations["English"])

st.markdown(lang_translations["ask_question"])

# Display buttons with preset prompts inside an expander
with st.expander(lang_translations["expander_title"]):
    for idx, button_text in enumerate(lang_translations["button_prompts"]):
        if st.button(button_text):
            st.session_state.prompt = lang_translations["prompts"][idx]

# Display existing chat messages
display_chat_messages()

# Render chat input widget. It appears disabled if processing is True.
typed_input = st.chat_input(
    lang_translations["typed_input_placeholder"],
    disabled=st.session_state.processing
)
# Update prompt if new input is provided
if typed_input and not st.session_state.processing:
    st.session_state.prompt = typed_input

# Process the prompt if one exists and we're not already processing a request
if st.session_state.prompt and not st.session_state.processing:
    st.session_state.processing = True
    additional_instructions = (
        f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of "
        f"{st.session_state.team} at the {st.session_state.school}. Please note that their native language is "
        f"{st.session_state.language}. THIS IS IMPORTANT ... When I ask a question or provide a response, please "
        f"respond in their native language regardless of the language they use to ask the question or provide a response. "
        "Pay special attention not to accidentally use words from another language when providing a response."
    )
    process_user_prompt(st.session_state.prompt, additional_instructions)