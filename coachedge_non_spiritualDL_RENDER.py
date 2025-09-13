# import openai
# import streamlit as st
# from openai import OpenAI
# import uuid
# import os

# client = OpenAI()

# st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# # Initialize session state variables
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if 'prompt' not in st.session_state:
#     st.session_state.prompt = ''
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

# # Grab the prompt from URL (if any)
# url_prompt = st.query_params.get("prompt", None)

# # Extract language from parentheses
# parts = st.session_state.language.split('(')
# if len(parts) > 1:
#     lang = parts[1].split(')')[0]
# else:
#     lang = "Unknown"

# additional_instructions = (
#     f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of "
#     f"{st.session_state.team} at the {st.session_state.school}. Please note that their native language is "
#     f"{st.session_state.language}. THIS IS IMPORTANT ... When they ask a question or provide a response, "
#     f"please respond in their native language regardless of the language they use to ask the question or provide the response. Pay special attention not to accidentally use words from another language when providing a response."
#     f"If native language is Unknown, default to English."
# )

# # Translation data
# translations = {
#     "English": {
#         "ask_question": "### **Ask Coach Edge**",
#         "typed_input_placeholder": "How else can I help?"
#     },
#     "Spanish": {
#         "ask_question": "### **Pregunta a Coach Edge**",
#         "typed_input_placeholder": "¿En qué más puedo ayudarte?"
#     },
#     "Arabic": {
#         "ask_question": "### **اسأل كوتش إيدج**",
#         "typed_input_placeholder": "كيف يمكنني مساعدتك بأمر آخر؟"
#     },
#     "Japanese": {
#         "ask_question": "### **Coach Edgeに質問する**",
#         "typed_input_placeholder": "他にどのようにお手伝いできますか？"
#     },
#     "French": {
#         "ask_question": "### **Demandez à Coach Edge**",
#         "typed_input_placeholder": "Comment puis-je vous aider autrement ?"
#     },
#     "Portuguese": {
#         "ask_question": "### **Pergunte ao Coach Edge**",
#         "typed_input_placeholder": "Como mais posso te ajudar?"
#     },
#     "Greek": {
#         "ask_question": "### **Ρωτήστε τον Coach Edge**",
#         "typed_input_placeholder": "Πώς αλλιώς μπορώ να βοηθήσω;"
#     },
#     "Dutch": {
#         "ask_question": "### **Vraag het Coach Edge**",
#         "typed_input_placeholder": "Waarmee kan ik verder helpen?"
#     },
#     "Swedish": {
#         "ask_question": "### **Fråga Coach Edge**",
#         "typed_input_placeholder": "Hur kan jag hjälpa dig ytterligare?"
#     },
#     "Bengali": {
#         "ask_question": "### **Coach Edgeকে জিজ্ঞাসা করুন**",
#         "typed_input_placeholder": "আপনাকে আর কীভাবে সাহায্য করতে পারি?"
#     },
#     "Hindi": {
#         "ask_question": "### **Coach Edge से पूछें**",
#         "typed_input_placeholder": "मैं और कैसे आपकी मदद कर सकता हूँ?"
#     },
#     "Ukrainian": {
#         "ask_question": "### **Запитайте Coach Edge**",
#         "typed_input_placeholder": "Чим ще я можу допомогти?"
#     },
#     "Indonesian": {
#         "ask_question": "### **Tanyakan kepada Coach Edge**",
#         "typed_input_placeholder": "Bagaimana lagi saya bisa membantu?"
#     }
# }

# # Use the detected language; fall back to English if none
# lang_translations = translations.get(lang, translations["English"])

# #st.markdown(lang_translations["ask_question"])

# # Text input for user (typed) prompt
# typed_input = st.chat_input(lang_translations["typed_input_placeholder"])

# # Decide which prompt to use: typed prompt (highest priority) or URL prompt (if typed is empty)
# if typed_input:
#     st.session_state.prompt = typed_input
# elif url_prompt:
#     st.session_state.prompt = url_prompt
# else:
#     st.session_state.prompt = ''

# # Display any past conversation messages first
# for message in st.session_state.messages:
#     if message["role"] == "user":
#         with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#             st.markdown(message["content"])
#     else:
#         with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#             st.markdown(message["content"])

# # If there's a new prompt to process
# if st.session_state.prompt:
#     # Add the user prompt to the message history
#     st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})

#     # Only display the user prompt if it was NOT provided via the URL
#     # (In other words, show it only if the user typed something.)
#     if typed_input:
#         with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#             st.markdown(st.session_state.prompt)

#     # Now generate the assistant's response
#     delta = []
#     response = ""
#     with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#         container = st.empty()

#         # Send user prompt to the OpenAI thread
#         st.session_state.thread_messages = client.beta.threads.messages.create(
#             st.session_state.thread.id, role="user", content=st.session_state.prompt
#         )

#         # Stream the assistant's response
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
#                         if content.type == 'text':
#                             delta.append(content.text.value)
#                             response = "".join(item for item in delta if item).strip()
#                             container.markdown(response)

#     # Save assistant's final response to message history
#     st.session_state.messages.append({"role": "assistant", "content": response}) 
#                                                           

import os
import streamlit as st
from openai import OpenAI

# ---------- Page config ----------
st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# ---------- Cache heavy/static things ----------
@st.cache_resource
def get_openai():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    assistant = client.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))
    return client, assistant

client, assistant = get_openai()

# ---------- Session state ----------
defaults = {
    "messages": [],
    "prompt": "",
    "fname": "",
    "school": "",
    "team": "",
    "role": "",
    "language": "",
    "thread_id": None,            # use ID only; no need to retrieve the object
    "consumed_url_prompt": False  # consume ?prompt= only once
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ---------- URL parameters ----------
params = st.query_params
st.session_state.fname = params.get("fname", st.session_state.fname or "Unknown")
st.session_state.school = params.get("school", st.session_state.school or "Unknown")
st.session_state.team = params.get("team", st.session_state.team or "Unknown")
st.session_state.role = params.get("role", st.session_state.role or "Unknown")
st.session_state.language = params.get("language", st.session_state.language or "Unknown")

url_thread_id = params.get("thread_id", None)
if url_thread_id and st.session_state.thread_id != url_thread_id:
    st.session_state.thread_id = url_thread_id

# Create a thread exactly once if we still don't have one
if not st.session_state.thread_id:
    st.session_state.thread_id = client.beta.threads.create().id

# Optional URL prompt (consume once so it doesn’t repeat on reruns)
url_prompt = params.get("prompt", None)
if url_prompt and not st.session_state.consumed_url_prompt:
    st.session_state.prompt = url_prompt
    st.session_state.consumed_url_prompt = True

# ---------- Language helpers ----------
def extract_language(lang_str: str) -> str:
    parts = lang_str.split("(")
    return parts[1].split(")")[0] if len(parts) > 1 else "Unknown"

lang_label = extract_language(st.session_state.language)


# ---------- Chat input ----------
typed_input = st.chat_input()
if typed_input:
    st.session_state.prompt = typed_input

# ---------- Show last N messages to keep UI fast ----------
MAX_UI_MESSAGES = 30
for msg in st.session_state.messages[-MAX_UI_MESSAGES:]:
    role = msg["role"]
    avatar = (
        "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
        if role == "user"
        else "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"
    )
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"])

# ---------- Process a new prompt ----------
if st.session_state.prompt:
    user_text = st.session_state.prompt

    # Add to UI history
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user", avatar="https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"):
        st.markdown(Thinking ...)

    # Add to thread (no retrieve needed)
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_text,
    )

    # Keep per-turn instructions short (put heavy policy in Assistant config)
    addl = (
        f"User name: {st.session_state.fname}. Role: {st.session_state.role}. "
        f"Team: {st.session_state.team}. School: {st.session_state.school}. "
        f"Native language: {lang_label}. If native language is 'Unknown', use English. "
        f"Always respond in the user's native language regardless of the language used in their message."
    )

    # Stream response with light throttling
    chunks, tick = [], 0
    with st.chat_message("assistant", avatar="https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"):
        container = st.empty()
        try:
            stream = client.beta.threads.runs.create(
                assistant_id=assistant.id,
                thread_id=st.session_state.thread_id,
                additional_instructions=addl,
                stream=True,
            )
            if stream:
                for event in stream:
                    if event.data.object == "thread.message.delta":
                        for c in event.data.delta.content:
                            if c.type == "text":
                                chunks.append(c.text.value)
                                tick += 1
                                if tick % 8 == 0:  # fewer DOM writes
                                    container.markdown("".join(chunks).strip())
        except Exception as e:
            chunks.append(f"\n\n_(Sorry, something went wrong: {e})_")

        # final flush
        assistant_text = "".join(chunks).strip() or "_(No response.)_"
        container.markdown(assistant_text)

    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
    st.session_state.prompt = ""