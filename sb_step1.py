import openai
import streamlit as st
from openai import OpenAI
import uuid
import requests

# ====== Adalo Save Function ===========
def save_answers (answer):
    payload = {
        "Season Builder Main": int(st.session_state.sb_id),
        "Answers": answer
    }
    headers = {
        "Authorization": ADALO_AUTH,
        "Content-Type": "application/json"
    }

    response = requests.post(ADALO_COLLECTION_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return {"status": "success", "data": response.json()}
    else:
        st.error(f"Failed to save to Adalo: {response.status_code}\n{response.text}")
        return {"status": "error", "detail": response.text}

client = OpenAI()

st.set_page_config(page_title="Coach Edge - Virtual Life Coach",layout="wide")

#Initialize session state variables

if "messages" not in st.session_state:
   st.session_state.messages = []

if 'prompt' not in st.session_state:
   st.session_state.prompt = ''

if 'fname' not in st.session_state:
    st.session_state.fname = ''  

if 'school' not in st.session_state:
    st.session_state.school = ''  

if 'team' not in st.session_state:
    st.session_state.team = ''  

if 'role' not in st.session_state:
    st.session_state.role = ''  

if 'language' not in st.session_state:
    st.session_state.language = ''  

if 'sb_id' not in st.session_state:
    st.session_state.sb_id = ''  

# ======== STREAMLIT SECRETS VARIABLES  ========
ADALO_COLLECTION_ID = st.secrets["ADALO_COLLECTION_ID"]
ADALO_APP_ID = st.secrets["ADALO_APP_ID"]
ADALO_API_KEY = st.secrets["ADALO_API_KEY"]
ADALO_COLLECTION_URL = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}"
ADALO_AUTH = f"Bearer {ADALO_API_KEY}"

# Initialize OpenAI assistant and thread
if "assistant" not in st.session_state or "thread" not in st.session_state:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])
    st.session_state.thread = client.beta.threads.create()
# >>>>>>>>>> NEW CODE STARTS HERE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Retrieve URL Parameters
st.session_state.fname = st.query_params.get("fname", "Unknown")
st.session_state.school = st.query_params.get("school", "Unknown")
st.session_state.team = st.query_params.get("team", "Unknown")
st.session_state.role = st.query_params.get("role", "Unknown")
st.session_state.language = st.query_params.get("language", "Unknown")
st.session_state.sb_id = st.query_params.get("sb_id", "Unknown")

# Grab the prompt from URL (if any)
url_prompt = st.query_params.get("prompt", None)

# Extract language from parentheses
parts = st.session_state.language.split('(')
if len(parts) > 1:
    lang = parts[1].split(')')[0]
else:
    lang = "Unknown"

additional_instructions = (
    f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of "
    f"{st.session_state.team} at the {st.session_state.school}. Please note that their native language is "
    f"{st.session_state.language}. THIS IS IMPORTANT ... When they ask a question or provide a response, "
    f"please respond in their native language regardless of the language they use to ask the question or provide the response. Pay special attention not to accidentally use words from another language when providing a response."
)

# Translation data
translations = {
    "English": {
        "ask_question": "### **Ask Coach Edge**",
        "typed_input_placeholder": "Type Answers Here"
    },
    "Spanish": {
        "ask_question": "### **Pregunta a Coach Edge**",
        "typed_input_placeholder": "Escribe tus respuestas aquí"
    },
    "Arabic": {
        "ask_question": "### **اسأل كوتش إيدج**",
        "typed_input_placeholder": "اكتب إجاباتك هنا"
    },
    "Japanese": {
        "ask_question": "### **Coach Edgeに質問する**",
        "typed_input_placeholder": "ここに回答を入力してください"
    },
    "French": {
        "ask_question": "### **Demandez à Coach Edge**",
        "typed_input_placeholder": "Tapez vos réponses ici"
    },
    "Portuguese": {
        "ask_question": "### **Pergunte ao Coach Edge**",
        "typed_input_placeholder": "Digite suas respostas aqui"
    },
    "Greek": {
        "ask_question": "### **Ρωτήστε τον Coach Edge**",
        "typed_input_placeholder": "Πληκτρολογήστε τις απαντήσεις σας εδώ"
    },
    "Dutch": {
        "ask_question": "### **Vraag het Coach Edge**",
        "typed_input_placeholder": "Typ hier je antwoorden"
    },
    "Swedish": {
        "ask_question": "### **Fråga Coach Edge**",
        "typed_input_placeholder": "Skriv dina svar här"
    },
    "Bengali": {
        "ask_question": "### **Coach Edgeকে জিজ্ঞাসা করুন**",
        "typed_input_placeholder": "এখানে আপনার উত্তর লিখুন"
    },
    "Hindi": {
        "ask_question": "### **Coach Edge से पूछें**",
        "typed_input_placeholder": "यहाँ अपने उत्तर टाइप करें"
    },
    "Ukrainian": {
        "ask_question": "### **Запитайте Coach Edge**",
        "typed_input_placeholder": "Введіть відповіді тут"
    },
    "Indonesian": {
        "ask_question": "### **Tanyakan kepada Coach Edge**",
        "typed_input_placeholder": "Ketik jawaban Anda di sini"
    }
}

# Use the detected language; fall back to English if none
lang_translations = translations.get(lang, translations["English"])

#st.markdown(lang_translations["ask_question"])

# Text input for user (typed) prompt
typed_input = st.chat_input(lang_translations["typed_input_placeholder"])


# Decide which prompt to use: typed prompt (highest priority) or URL prompt (if typed is empty)
if typed_input:
    st.session_state.prompt = typed_input
    if st.session_state.sb_id != "Unknown":
        save_answers (answer=typed_input)
elif url_prompt:
    st.session_state.prompt = url_prompt
else:
    st.session_state.prompt = ''

# Display any past conversation messages first
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
            st.markdown(message["content"])
    else:
        with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
            st.markdown(message["content"])

# If there's a new prompt to process
if st.session_state.prompt:
    # Add the user prompt to the message history
    st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})

    # Only display the user prompt if it was NOT provided via the URL
    # (In other words, show it only if the user typed something.)
    if typed_input:
        with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
            st.markdown(st.session_state.prompt)

    # Now generate the assistant's response
    delta = []
    response = ""
    with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
        container = st.empty()

        # Send user prompt to the OpenAI thread
        st.session_state.thread_messages = client.beta.threads.messages.create(
            st.session_state.thread.id, role="user", content=st.session_state.prompt
        )

        # Stream the assistant's response
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
                        if content.type == 'text':
                            delta.append(content.text.value)
                            response = "".join(item for item in delta if item).strip()
                            container.markdown(response)

    # Save assistant's final response to message history
    st.session_state.messages.append({"role": "assistant", "content": response}) 
 
 # ==============  CODE THAT WAS GOING TO TRY TO USE THE ASSISTANTS FUNCTION ======================
# import openai
# import streamlit as st
# import os
# import json
# import requests
# import time

# # ======== ENV VARIABLES (set these in your environment or .env) ========
# # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# # ADALO_COLLECTION_ID = os.getenv("ADALO_COLLECTION_ID")
# # ADALO_APP_ID = os.getenv("ADALO_APP_ID")
# # ADALO_API_KEY = os.getenv("ADALO_API_KEY")
# # ADALO_COLLECTION_URL = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}"
# # ADALO_AUTH = f"Bearer {ADALO_API_KEY}"
# # OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT")  # Your already-created assistant (string)

# # ======== STREAMLIT SECRETS VARIABLES  ========
# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# ADALO_COLLECTION_ID = st.secrets["ADALO_COLLECTION_ID"]
# ADALO_APP_ID = st.secrets["ADALO_APP_ID"]
# ADALO_API_KEY = st.secrets["ADALO_API_KEY"]
# ADALO_COLLECTION_URL = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}"
# ADALO_AUTH = f"Bearer {ADALO_API_KEY}"
# OPENAI_ASSISTANT_ID = st.secrets["OPENAI_ASSISTANT"]  # Your already-created assistant (string)


# openai.api_key = OPENAI_API_KEY
# client = openai.OpenAI()

# # ====== Adalo Save Function ===========
# def save_answers_to_adalo(sb_id, answers):
#     payload = {
#         "SB_ID": sb_id,
#         "Answers": json.dumps(answers)
#     }
#     headers = {
#         "Authorization": ADALO_AUTH,
#         "Content-Type": "application/json"
#     }
#     response = requests.post(ADALO_COLLECTION_URL, headers=headers, json=payload)
#     if response.status_code == 201:
#         return {"status": "success", "data": response.json()}
#     else:
#         st.error(f"Failed to save to Adalo: {response.status_code}\n{response.text}")
#         return {"status": "error", "detail": response.text}

# # ====== Streamlit State Vars ==========
# st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# params = st.query_params

# st.session_state.fname = params.get("fname", "Unknown")
# st.session_state.school = params.get("school", "Unknown")
# st.session_state.team = params.get("team", "Unknown")
# st.session_state.role = params.get("role", "Unknown")
# st.session_state.language = params.get("language", "Unknown")
# st.session_state.sb_id = params.get("sb_id", "Unknown")

# # # Grab the prompt from URL (if any)
# url_prompt = st.query_params.get("prompt", None)

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if 'prompt' not in st.session_state:
#     st.session_state.prompt = ''

# if "assistant" not in st.session_state:
#     # Retrieve Assistant you already created
#     st.session_state.assistant = openai.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)

# if "thread" not in st.session_state:
#     st.session_state.thread = client.beta.threads.create()

# # ====== Language Placeholder ======
# lang = st.session_state.language
# translations = {
#     "English": {"typed_input_placeholder": "Type Answers Here"},
#     "Spanish": {"typed_input_placeholder": "Escribe tus respuestas aquí"},
#     # Add more if needed
# }
# lang_translations = translations.get(lang, translations["English"])

# # ====== Show Chat Session So Far ==========
# typed_input = st.chat_input(lang_translations["typed_input_placeholder"])
# # Decide which prompt to use: typed prompt (highest priority) or URL prompt (if typed is empty)
# if typed_input:
#     st.session_state.prompt = typed_input
# elif url_prompt:
#     st.session_state.prompt = url_prompt
# else:
#     st.session_state.prompt = ''

# for message in st.session_state.messages:
#     if message["role"] == "user":
#         with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#             st.markdown(message["content"])
#     elif message["role"] == "assistant":
#         with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#             st.markdown(message["content"])

# # ====== Function Call Handler (for function tool) ======
# def handle_run_and_function_calls(thread_id, run_id, sb_id_default):
#     # Poll the run for status/function call
#     while True:
#         run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
#         if run.status in ('completed', 'failed', 'cancelled'):
#             break
#         elif run.status == "requires_action":
#             tool_calls = run.required_action.submit_tool_outputs.tool_calls
#             tool_outputs = []
#             for tool_call in tool_calls:
#                 fn_name = tool_call.function.name
#                 fn_args = json.loads(tool_call.function.arguments)
#                 if fn_name == "save_answers_to_adalo":
#                     # If sb_id is missing, supply from session state
#                     if not fn_args.get('sb_id') or fn_args["sb_id"] == "Unknown":
#                         fn_args["sb_id"] = sb_id_default
#                     adalo_result = save_answers_to_adalo(fn_args["sb_id"], fn_args["answers"])
#                     tool_outputs.append({
#                         "tool_call_id": tool_call.id,
#                         "output": json.dumps(adalo_result)
#                     })
#             client.beta.threads.runs.submit_tool_outputs(
#                 thread_id=thread_id,
#                 run_id=run_id,
#                 tool_outputs=tool_outputs
#             )
#         else:
#             time.sleep(1)

# # ====== Core Chat Logic ======
# if st.session_state.prompt:
#     # Add user message to chat
#     st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
#     with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#         st.markdown(st.session_state.prompt)

#     # Create OpenAI thread message
#     client.beta.threads.messages.create(
#         st.session_state.thread.id, role="user", content=st.session_state.prompt
#     )

#     # Start a run (do NOT register tools—your Assistant already has the tool)
#     additional_instructions = (
#         f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of "
#         f"{st.session_state.team} at {st.session_state.school}. Please note their native language is "
#         f"{st.session_state.language}. The sb_id for the database is {st.session_state.sb_id}."
#     )
#     run = client.beta.threads.runs.create(
#         assistant_id=st.session_state.assistant.id,
#         thread_id=st.session_state.thread.id,
#         additional_instructions=additional_instructions,
#         stream=False # required for function tool
#     )

#     # Handle function tool call if one is made
#     handle_run_and_function_calls(
#         thread_id=st.session_state.thread.id,
#         run_id=run.id,
#         sb_id_default=st.session_state.sb_id
#     )

#     # Get the updated assistant messages and display only the latest reply
#     messages = client.beta.threads.messages.list(thread_id=st.session_state.thread.id)
#     for msg in messages.data[::-1]:
#         if msg.role == "assistant":
#             # OpenAI responses have content as a list of blocks
#             reply_text = ""
#             if len(msg.content) and hasattr(msg.content[0],'text'):
#                 reply_text = msg.content[0].text.value
#             st.session_state.messages.append({"role": "assistant", "content": reply_text})
#             with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#                 st.markdown(reply_text)
#             break  # only display one latest assistant reply                                                                                                                                                          