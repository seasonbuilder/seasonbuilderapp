import os
import requests
import streamlit as st
from openai import OpenAI

# ====== Adalo Save Function ===========
def save_answers(answer: str):
    payload = {
        "Season Builder Main": int(st.session_state.sb_id),
        "Answers": answer
    }
    headers = {
        "Authorization": ADALO_AUTH,
        "Content-Type": "application/json"
    }
    try:
        requests.post(ADALO_COLLECTION_URL, headers=headers, json=payload, timeout=10)
    except requests.RequestException:
        # Keep UX smooth; optionally log
        pass

# ---------- Page config ----------
st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# ---------- OpenAI client ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PROMPT_ID = os.getenv("OPENAI_PROMPT_ID")  # e.g., "prompt_abc123"

# ======== ENV VARIABLES  ========
ADALO_COLLECTION_ID = os.getenv("ADALO_COLLECTION_ID")
ADALO_APP_ID = os.getenv("ADALO_APP_ID") or os.getenv("APP_ID")  # support either name
ADALO_API_KEY = os.getenv("ADALO_API_KEY")
ADALO_COLLECTION_URL = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}"
ADALO_AUTH = f"Bearer {ADALO_API_KEY}"

# ---------- Session state ----------
ss = st.session_state
for key, default in {
    "messages": [],
    "prompt": "",
    "fname": "",
    "school": "",
    "team": "",
    "role": "",
    "language": "",
    "sb_id": "",
    "conversation_id": None,       # replaces thread
    "consumed_url_prompt": False,  # consume ?prompt= once
}.items():
    ss.setdefault(key, default)

# >>>>>>>>>> NEW CODE STARTS HERE (Prompt + Conversations) <<<<<<<<<<<<<<

# Retrieve URL Parameters
qp = st.query_params
ss.fname    = qp.get("fname",    ss.fname or "Unknown")
ss.school   = qp.get("school",   ss.school or "Unknown")
ss.team     = qp.get("team",     ss.team or "Unknown")
ss.role     = qp.get("role",     ss.role or "Unknown")
ss.language = qp.get("language", ss.language or "Unknown")
ss.sb_id    = qp.get("sb_id",    ss.sb_id or "Unknown")

# Optional: support resuming a conversation if passed in URL
passed_conversation_id = qp.get("conversation_id") or None
if passed_conversation_id and ss.conversation_id != passed_conversation_id:
    ss.conversation_id = passed_conversation_id

# Create a conversation once if we still don't have one
if not ss.conversation_id:
    conv = client.conversations.create()
    ss.conversation_id = conv.id

# Grab the prompt from URL (consume once so it doesn’t repeat on reruns)
url_prompt = qp.get("prompt", None)
if url_prompt and not ss.consumed_url_prompt:
    ss.prompt = url_prompt
    ss.consumed_url_prompt = True

# Extract language from parentheses
parts = (ss.language or "").split("(")
lang = parts[1].split(")")[0] if len(parts) > 1 else "Unknown"

# Translation data
translations = {
    "English":    {"ask_question": "### **Ask Coach Edge**", "typed_input_placeholder": "Type Answers Here"},
    "Spanish":    {"ask_question": "### **Pregunta a Coach Edge**", "typed_input_placeholder": "Escribe tus respuestas aquí"},
    "Arabic":     {"ask_question": "### **اسأل كوتش إيدج**", "typed_input_placeholder": "اكتب إجاباتك هنا"},
    "Japanese":   {"ask_question": "### **Coach Edgeに質問する**", "typed_input_placeholder": "ここに回答を入力してください"},
    "French":     {"ask_question": "### **Demandez à Coach Edge**", "typed_input_placeholder": "Tapez vos réponses ici"},
    "Portuguese": {"ask_question": "### **Pergunte ao Coach Edge**", "typed_input_placeholder": "Digite suas respostas aqui"},
    "Greek":      {"ask_question": "### **Ρωτήστε τον Coach Edge**", "typed_input_placeholder": "Πληκτρολογήστε τις απαντήσεις σας εδώ"},
    "Dutch":      {"ask_question": "### **Vraag het Coach Edge**", "typed_input_placeholder": "Typ hier je antwoorden"},
    "Swedish":    {"ask_question": "### **Fråga Coach Edge**", "typed_input_placeholder": "Skriv dina svar här"},
    "Bengali":    {"ask_question": "### **Coach Edgeকে জিজ্ঞাসা করুন**", "typed_input_placeholder": "এখানে আপনার উত্তর লিখুন"},
    "Hindi":      {"ask_question": "### **Coach Edge से पूछें**", "typed_input_placeholder": "यहाँ अपने उत्तर टाइप करें"},
    "Ukrainian":  {"ask_question": "### **Запитайте Coach Edge**", "typed_input_placeholder": "Введіть відповіді тут"},
    "Indonesian": {"ask_question": "### **Tanyakan kepada Coach Edge**", "typed_input_placeholder": "Ketik jawaban Anda di sini"},
}
lang_translations = translations.get(lang, translations["English"])

# UI header (optional)
# st.markdown(lang_translations["ask_question"])

# Text input for user (typed) prompt
typed_input = st.chat_input(lang_translations["typed_input_placeholder"])

# Decide which prompt to use: typed prompt (highest priority) or URL prompt
if typed_input:
    ss.prompt = typed_input
    if ss.sb_id != "Unknown":
        save_answers(answer=typed_input)
elif url_prompt:
    ss.prompt = url_prompt
else:
    ss.prompt = ''

# Display any past conversation messages first
USER_AVATAR = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
ASSISTANT_AVATAR = "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"
for message in ss.messages:
    role = message["role"]
    avatar = USER_AVATAR if role == "user" else ASSISTANT_AVATAR
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

# If there's a new prompt to process
if ss.prompt:
    # Add the user prompt to the message history
    ss.messages.append({"role": "user", "content": ss.prompt})

    # Only display the user prompt if it was typed (echo behavior matches your original)
    if typed_input:
        with st.chat_message('user', avatar=USER_AVATAR):
            st.markdown(ss.prompt)

    # Build per-turn system context + user item
    system_context = (
        f"User name: {ss.fname}. They are a {ss.role} in the sport of {ss.team} at {ss.school}. "
        f"Native language: {ss.language}. "
        f"Always respond in the user's native language regardless of the language they use; "
        f"if native language is 'Unknown', use English. Do not mix languages inadvertently."
    )
    input_items = [
        {"role": "system", "content": system_context},
        {"role": "user",   "content": ss.prompt},
    ]

    # Stream the assistant's response via Responses API using your Chat Prompt ID + Conversation
    delta = []
    response = ""
    with st.chat_message('assistant', avatar=ASSISTANT_AVATAR):
        container = st.empty()
        try:
            stream = client.responses.create(
                prompt={"id": PROMPT_ID},            # Use your Chat Prompt (model/tools/instructions)
                conversation=ss.conversation_id,     # Keep context like Threads did
                input=input_items,                   # Per-turn items (system + user)
                stream=True
            )
            if stream:
                for event in stream:
                    # canonical streaming delta for Responses API
                    if getattr(event, "type", "") == "response.output_text.delta":
                        delta.append(event.delta)
                        # throttle UI writes a bit
                        if len(delta) % 8 == 0:
                            response = "".join(delta).strip()
                            container.markdown(response)
        except Exception as e:
            delta.append(f"\n\n_(Sorry, something went wrong: {e})_")

        # Final flush
        response = "".join(delta).strip()
        container.markdown(response or "_(No response.)_")

    # Save assistant's final response to message history
    ss.messages.append({"role": "assistant", "content": response})
    # Clear prompt
    ss.prompt = ""

# import openai
# import streamlit as st
# from openai import OpenAI
# import uuid
# import os
# import requests

# # ====== Adalo Save Function ===========
# def save_answers (answer):
#     payload = {
#         "Season Builder Main": int(st.session_state.sb_id),
#         "Answers": answer
#     }
#     headers = {
#         "Authorization": ADALO_AUTH,
#         "Content-Type": "application/json"
#     }

#     response = requests.post(ADALO_COLLECTION_URL, headers=headers, json=payload)
#     # if response.status_code == 200:
#     #     return {"status": "success", "data": response.json()}
#     # else:
#     #     st.error(f"Failed to save to Adalo: {response.status_code}\n{response.text}")
#     #     return {"status": "error", "detail": response.text}

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

# if 'sb_id' not in st.session_state:
#     st.session_state.sb_id = ''  

# # ======== ENV VARIABLES  ========
# ADALO_COLLECTION_ID = os.getenv("ADALO_COLLECTION_ID")
# ADALO_APP_ID = os.getenv("ADALO_APP_ID")
# ADALO_API_KEY = os.getenv("ADALO_API_KEY")
# ADALO_COLLECTION_URL = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}"
# ADALO_AUTH = f"Bearer {ADALO_API_KEY}"

# # Initialize OpenAI assistant and thread
# if "assistant" not in st.session_state or "thread" not in st.session_state:
#     openai.api_key = os.getenv("OPENAI_API_KEY")
#     st.session_state.assistant = openai.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))
#     st.session_state.thread = client.beta.threads.create()

# # >>>>>>>>>> NEW CODE STARTS HERE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# # Retrieve URL Parameters
# st.session_state.fname = st.query_params.get("fname", "Unknown")
# st.session_state.school = st.query_params.get("school", "Unknown")
# st.session_state.team = st.query_params.get("team", "Unknown")
# st.session_state.role = st.query_params.get("role", "Unknown")
# st.session_state.language = st.query_params.get("language", "Unknown")
# st.session_state.sb_id = st.query_params.get("sb_id", "Unknown")

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
# )

# # Translation data
# translations = {
#     "English": {
#         "ask_question": "### **Ask Coach Edge**",
#         "typed_input_placeholder": "Type Answers Here"
#     },
#     "Spanish": {
#         "ask_question": "### **Pregunta a Coach Edge**",
#         "typed_input_placeholder": "Escribe tus respuestas aquí"
#     },
#     "Arabic": {
#         "ask_question": "### **اسأل كوتش إيدج**",
#         "typed_input_placeholder": "اكتب إجاباتك هنا"
#     },
#     "Japanese": {
#         "ask_question": "### **Coach Edgeに質問する**",
#         "typed_input_placeholder": "ここに回答を入力してください"
#     },
#     "French": {
#         "ask_question": "### **Demandez à Coach Edge**",
#         "typed_input_placeholder": "Tapez vos réponses ici"
#     },
#     "Portuguese": {
#         "ask_question": "### **Pergunte ao Coach Edge**",
#         "typed_input_placeholder": "Digite suas respostas aqui"
#     },
#     "Greek": {
#         "ask_question": "### **Ρωτήστε τον Coach Edge**",
#         "typed_input_placeholder": "Πληκτρολογήστε τις απαντήσεις σας εδώ"
#     },
#     "Dutch": {
#         "ask_question": "### **Vraag het Coach Edge**",
#         "typed_input_placeholder": "Typ hier je antwoorden"
#     },
#     "Swedish": {
#         "ask_question": "### **Fråga Coach Edge**",
#         "typed_input_placeholder": "Skriv dina svar här"
#     },
#     "Bengali": {
#         "ask_question": "### **Coach Edgeকে জিজ্ঞাসা করুন**",
#         "typed_input_placeholder": "এখানে আপনার উত্তর লিখুন"
#     },
#     "Hindi": {
#         "ask_question": "### **Coach Edge से पूछें**",
#         "typed_input_placeholder": "यहाँ अपने उत्तर टाइप करें"
#     },
#     "Ukrainian": {
#         "ask_question": "### **Запитайте Coach Edge**",
#         "typed_input_placeholder": "Введіть відповіді тут"
#     },
#     "Indonesian": {
#         "ask_question": "### **Tanyakan kepada Coach Edge**",
#         "typed_input_placeholder": "Ketik jawaban Anda di sini"
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
#     if st.session_state.sb_id != "Unknown":
#         save_answers (answer=typed_input)
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