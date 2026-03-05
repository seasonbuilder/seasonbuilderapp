# import os
# import requests
# import streamlit as st
# from openai import OpenAI
# from translations_spiritual import translations as T  # external translations

# # ---------- Page config ----------
# st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# # ---------- Constants ----------
# USER_AVATAR = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
# ASSISTANT_AVATAR = "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"
# MAX_UI_MESSAGES = 30

# # ---------- Prompt routing (SB / CB) ----------
# PROMPT_ID_SB = os.getenv("OPENAI_PROMPT_ID_SB") or os.getenv("OPENAI_PROMPT_ID")
# PROMPT_ID_CB = os.getenv("OPENAI_PROMPT_ID_CB") or os.getenv("OPENAI_PROMPT_ID")

# # Responses API currently still requires `model`
# OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# # ---------- Cache heavy/static things ----------
# @st.cache_resource(show_spinner=False)
# def get_openai():
#     return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# @st.cache_resource(show_spinner=False)
# def get_http_session():
#     s = requests.Session()
#     s.headers.update({"Content-Type": "application/json"})
#     return s

# @st.cache_data(show_spinner=False)
# def get_translations():
#     return T

# client = get_openai()
# http = get_http_session()
# LANGS = get_translations()

# # ---------- Session state ----------
# ss = st.session_state
# ss.setdefault("messages", [])
# ss.setdefault("fname", "")
# ss.setdefault("school", "")
# ss.setdefault("team", "")
# ss.setdefault("role", "")
# ss.setdefault("language", "")

# # Option A flags
# ss.setdefault("submitted_prompt", "")
# ss.setdefault("processing", False)
# ss.setdefault("prompt_source", "")        # "chat" | "url" | "button"
# ss.setdefault("consumed_url_prompt", False)

# # Conversations + Adalo sync
# ss.setdefault("conversation_id", None)
# ss.setdefault("adalo_synced", False)

# # ---------- URL parameters (backward compatible) ----------
# qp = st.query_params

# ss.fname    = qp.get("fname",    ss.fname or "Unknown")
# ss.school   = qp.get("school",   ss.school or "Unknown")
# ss.team     = qp.get("team",     ss.team or "Unknown")
# ss.role     = qp.get("role",     ss.role or "Unknown")
# ss.language = qp.get("language", ss.language or "Unknown")

# email = qp.get("email") or ""

# # NEW param: program (defaults to SB)
# program = (qp.get("program") or "SB").strip().upper()
# if program not in ("SB", "CB"):
#     program = "SB"
# PROMPT_ID = PROMPT_ID_SB if program == "SB" else PROMPT_ID_CB

# # Option A migration behavior:
# # resume ONLY if conversation_id exists; ignore legacy thread_id entirely
# passed_convo_id = qp.get("conversation_id") or None
# if passed_convo_id and ss.conversation_id != passed_convo_id:
#     ss.conversation_id = passed_convo_id

# # ---------- Adalo sync (only when we create a new conversation) ----------
# def update_adalo_user_conversation_once(email_: str, conversation_id_: str):
#     if not email_ or not conversation_id_ or ss.adalo_synced:
#         return

#     app_id = os.getenv("APP_ID")
#     col_id = os.getenv("ADALO_COLLECTION_ID")
#     api_key = os.getenv("ADALO_API_KEY")
#     if not (app_id and col_id and api_key):
#         return

#     headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
#     base = f"https://api.adalo.com/v0/apps/{app_id}/collections/{col_id}"

#     # assumes you created a column named conversation_id in Adalo Users
#     payload = {"conversation_id": conversation_id_}

#     try:
#         r = http.get(f"{base}?filterKey=Email&filterValue={email_}", headers=headers, timeout=10)
#         if r.status_code != 200:
#             return
#         data = r.json()
#         records = data.get("records") or []
#         if not records:
#             return
#         element_id = records[0].get("id")
#         if not element_id:
#             return

#         upd = http.put(f"{base}/{element_id}", json=payload, headers=headers, timeout=10)
#         if upd.status_code == 200:
#             ss.adalo_synced = True
#     except requests.RequestException:
#         pass

# # ---------- Conversation bootstrapping ----------
# def ensure_conversation():
#     if ss.conversation_id:
#         return
#     conv = client.conversations.create()
#     ss.conversation_id = conv.id
#     update_adalo_user_conversation_once(email, conv.id)

# ensure_conversation()

# # ---------- Language helpers ----------
# def extract_language(label: str) -> str:
#     parts = label.split("(")
#     return parts[1].split(")")[0] if len(parts) > 1 else "Unknown"

# def t_for(lang_label: str) -> dict:
#     return LANGS.get(lang_label, LANGS.get("English", {}))

# def tkey(lang_dict: dict, key: str, default: str) -> str:
#     return lang_dict.get(key, default)

# lang_label = extract_language(ss.language)
# LANG = t_for(lang_label)

# url_prompt = qp.get("prompt")
# use_translations_ui = not bool(url_prompt)

# if use_translations_ui:
#     ask_q = tkey(LANG, "ask_question", "### **Ask Coach Edge**")
#     expander_title = tkey(LANG, "expander_title", "Topics To Get You Started")
#     button_prompts = LANG.get("button_prompts", [])
#     button_prompt_vals = LANG.get("prompts", [])
#     placeholder = tkey(LANG, "typed_input_placeholder", "How else can I help?")
# else:
#     ask_q = ""
#     expander_title = ""
#     button_prompts = []
#     button_prompt_vals = []
#     placeholder = "How else can I help?"

# # ---------- Build per-turn system context ----------
# def build_system_context() -> str:
#     return (
#         f"User name: {ss.fname}. "
#         f"Role: {ss.role}. Team: {ss.team}. School: {ss.school}. "
#         f"Native language: {lang_label}. "
#         f"Always respond in the user's native language; if 'Unknown', use English. "
#         f"Do not mix languages inadvertently."
#     )

# # ---------- PROCESS FIRST (Option A) ----------
# def process_user_prompt(prompt_text: str, echo_user: bool):
#     # Only echo if it came from chat_input
#     if echo_user:
#         ss.messages.append({"role": "user", "content": prompt_text})
#         with st.chat_message("user", avatar=USER_AVATAR):
#             st.markdown(prompt_text)

#     input_items = [
#         {"role": "system", "content": build_system_context()},
#         {"role": "user",   "content": prompt_text},
#     ]

#     chunks, tick = [], 0
#     with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
#         container = st.empty()
#         try:
#             stream = client.responses.create(
#                 prompt={"id": PROMPT_ID},
#                 conversation=ss.conversation_id,
#                 input=input_items,
#                 stream=True,
#                 store=True
#             )
#             for event in stream:
#                 etype = getattr(event, "type", "")
#                 if etype == "response.output_text.delta":
#                     chunks.append(event.delta)
#                     tick += 1
#                     if tick % 8 == 0:
#                         container.markdown("".join(chunks).strip())
#         except Exception as e:
#             chunks.append(f"\n\n_(Sorry, something went wrong: {e})_")

#         assistant_text = "".join(chunks).strip() or "_(No response.)_"
#         container.markdown(assistant_text)

#     ss.messages.append({"role": "assistant", "content": assistant_text})

#     ss.submitted_prompt = ""
#     ss.processing = False
#     ss.prompt_source = ""

# # =========================================================
# # UI ORDER FIX:
# # 1) header/buttons
# # 2) history
# # 3) process queued prompt (in the right spot)
# # 4) chat_input last
# # =========================================================

# # ---------- Header/buttons ----------
# if ask_q:
#     st.markdown(ask_q)

# if use_translations_ui:
#     with st.expander(expander_title):
#         for idx, button_text in enumerate(button_prompts):
#             if st.button(button_text):
#                 if idx < len(button_prompt_vals):
#                     ss.submitted_prompt = button_prompt_vals[idx]
#                     ss.processing = True
#                     ss.prompt_source = "button"

# # ---------- Show last N messages ----------
# for m in ss.messages[-MAX_UI_MESSAGES:]:
#     avatar = USER_AVATAR if m["role"] == "user" else ASSISTANT_AVATAR
#     with st.chat_message(m["role"], avatar=avatar):
#         st.markdown(m["content"])

# # ---------- Consume URL prompt once (do NOT echo) ----------
# if url_prompt and not ss.consumed_url_prompt and not ss.processing:
#     ss.submitted_prompt = url_prompt
#     ss.processing = True
#     ss.prompt_source = "url"
#     ss.consumed_url_prompt = True

# # ---------- If a prompt is waiting, handle it NOW (after history) ----------
# if ss.submitted_prompt and ss.processing:
#     echo = (ss.prompt_source == "chat")  # ONLY chat_input echoes
#     process_user_prompt(ss.submitted_prompt, echo_user=echo)

# # ---------- Chat input LAST ----------
# def on_submit():
#     ss.submitted_prompt = ss.user_input
#     ss.processing = True
#     ss.prompt_source = "chat"

# if ss.processing:
#     st.chat_input(placeholder, disabled=True)
# else:
#     _ = st.chat_input(
#         placeholder,
#         key="user_input",
#         on_submit=on_submit
#     )

import os
import requests
import streamlit as st
from openai import OpenAI
from translations_spiritual import translations as T  # external translations

# ---------- Page config ----------
st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# ---------- Constants ----------
USER_AVATAR = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
ASSISTANT_AVATAR = "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"
MAX_UI_MESSAGES = 30

# ---------- Prompt routing (SB / CB) ----------
PROMPT_ID_SB = os.getenv("OPENAI_PROMPT_ID_SB") or os.getenv("OPENAI_PROMPT_ID")
PROMPT_ID_CB = os.getenv("OPENAI_PROMPT_ID_CB") or os.getenv("OPENAI_PROMPT_ID")

# Responses API currently still requires `model`
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# ---------- Cache heavy/static things ----------
@st.cache_resource(show_spinner=False)
def get_openai():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@st.cache_resource(show_spinner=False)
def get_http_session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s

@st.cache_data(show_spinner=False)
def get_translations():
    return T

client = get_openai()
http = get_http_session()
LANGS = get_translations()

# ---------- Session state ----------
ss = st.session_state
ss.setdefault("messages", [])
ss.setdefault("fname", "")
ss.setdefault("school", "")
ss.setdefault("team", "")
ss.setdefault("role", "")
ss.setdefault("language", "")

# Option A flags
ss.setdefault("submitted_prompt", "")
ss.setdefault("processing", False)
ss.setdefault("prompt_source", "")        # "chat" | "url" | "button"
ss.setdefault("consumed_url_prompt", False)

# Conversations + Adalo sync
ss.setdefault("conversation_id", None)
ss.setdefault("adalo_synced", False)

# ---------- URL parameters (backward compatible) ----------
qp = st.query_params

ss.fname    = qp.get("fname",    ss.fname or "Unknown")
ss.school   = qp.get("school",   ss.school or "Unknown")
ss.team     = qp.get("team",     ss.team or "Unknown")
ss.role     = qp.get("role",     ss.role or "Unknown")
ss.language = qp.get("language", ss.language or "Unknown")

email = qp.get("email") or ""

# NEW param: program (defaults to SB)
program = (qp.get("program") or "SB").strip().upper()
if program not in ("SB", "CB"):
    program = "SB"
PROMPT_ID = PROMPT_ID_SB if program == "SB" else PROMPT_ID_CB

# resume ONLY if conversation_id exists; ignore legacy thread_id entirely
passed_convo_id = qp.get("conversation_id") or None
if passed_convo_id and ss.conversation_id != passed_convo_id:
    ss.conversation_id = passed_convo_id

# ---------- Role helper ----------
def is_athlete_role(role_str: str) -> bool:
    """
    Returns True if the role represents an athlete.
    Handles: "Athlete", "athlete", "Athlete (Soccer)", "athlete - captain", etc.
    """
    if not role_str:
        return False
    role_norm = role_str.strip().lower()
    return role_norm == "athlete" or role_norm.startswith("athlete")

# ---------- Adalo sync (only when we create a new conversation) ----------
def update_adalo_user_conversation_once(email_: str, conversation_id_: str):
    # >>> KEY CHANGE: do not store conversation_id for athletes <<<
    if is_athlete_role(ss.role):
        return

    if not email_ or not conversation_id_ or ss.adalo_synced:
        return

    app_id = os.getenv("APP_ID")
    col_id = os.getenv("ADALO_COLLECTION_ID")
    api_key = os.getenv("ADALO_API_KEY")
    if not (app_id and col_id and api_key):
        return

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    base = f"https://api.adalo.com/v0/apps/{app_id}/collections/{col_id}"

    # assumes you created a column named conversation_id in Adalo Users
    payload = {"conversation_id": conversation_id_}

    try:
        r = http.get(f"{base}?filterKey=Email&filterValue={email_}", headers=headers, timeout=10)
        if r.status_code != 200:
            return
        data = r.json()
        records = data.get("records") or []
        if not records:
            return
        element_id = records[0].get("id")
        if not element_id:
            return

        upd = http.put(f"{base}/{element_id}", json=payload, headers=headers, timeout=10)
        if upd.status_code == 200:
            ss.adalo_synced = True
    except requests.RequestException:
        pass

# ---------- Conversation bootstrapping ----------
def ensure_conversation():
    if ss.conversation_id:
        return
    conv = client.conversations.create()
    ss.conversation_id = conv.id
    update_adalo_user_conversation_once(email, conv.id)

ensure_conversation()

# ---------- Language helpers ----------
def extract_language(label: str) -> str:
    parts = label.split("(")
    return parts[1].split(")")[0] if len(parts) > 1 else "Unknown"

def t_for(lang_label: str) -> dict:
    return LANGS.get(lang_label, LANGS.get("English", {}))

def tkey(lang_dict: dict, key: str, default: str) -> str:
    return lang_dict.get(key, default)

lang_label = extract_language(ss.language)
LANG = t_for(lang_label)

url_prompt = qp.get("prompt")
use_translations_ui = not bool(url_prompt)

if use_translations_ui:
    ask_q = tkey(LANG, "ask_question", "### **Ask Coach Edge**")
    expander_title = tkey(LANG, "expander_title", "Topics To Get You Started")
    button_prompts = LANG.get("button_prompts", [])
    button_prompt_vals = LANG.get("prompts", [])
    placeholder = tkey(LANG, "typed_input_placeholder", "How else can I help?")
else:
    ask_q = ""
    expander_title = ""
    button_prompts = []
    button_prompt_vals = []
    placeholder = "How else can I help?"

# ---------- Build per-turn system context ----------
def build_system_context() -> str:
    return (
        f"User name: {ss.fname}. "
        f"Role: {ss.role}. Team: {ss.team}. School: {ss.school}. "
        f"Native language: {lang_label}. "
        f"Always respond in the user's native language; if 'Unknown', use English. "
        f"Do not mix languages inadvertently."
    )

# ---------- PROCESS FIRST (Option A) ----------
def process_user_prompt(prompt_text: str, echo_user: bool):
    if echo_user:
        ss.messages.append({"role": "user", "content": prompt_text})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt_text)

    input_items = [
        {"role": "system", "content": build_system_context()},
        {"role": "user",   "content": prompt_text},
    ]

    chunks, tick = [], 0
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        container = st.empty()
        try:
            stream = client.responses.create(
                model=OPENAI_MODEL,
                prompt={"id": PROMPT_ID},
                conversation=ss.conversation_id,
                input=input_items,
                stream=True,
                store=True
            )
            for event in stream:
                etype = getattr(event, "type", "")
                if etype == "response.output_text.delta":
                    chunks.append(event.delta)
                    tick += 1
                    if tick % 8 == 0:
                        container.markdown("".join(chunks).strip())
        except Exception as e:
            chunks.append(f"\n\n_(Sorry, something went wrong: {e})_")

        assistant_text = "".join(chunks).strip() or "_(No response.)_"
        container.markdown(assistant_text)

    ss.messages.append({"role": "assistant", "content": assistant_text})

    ss.submitted_prompt = ""
    ss.processing = False
    ss.prompt_source = ""

# ---------- Header/buttons ----------
if ask_q:
    st.markdown(ask_q)

if use_translations_ui:
    with st.expander(expander_title):
        for idx, button_text in enumerate(button_prompts):
            if st.button(button_text):
                if idx < len(button_prompt_vals):
                    ss.submitted_prompt = button_prompt_vals[idx]
                    ss.processing = True
                    ss.prompt_source = "button"

# ---------- Show last N messages ----------
for m in ss.messages[-MAX_UI_MESSAGES:]:
    avatar = USER_AVATAR if m["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

# ---------- Consume URL prompt once (do NOT echo) ----------
if url_prompt and not ss.consumed_url_prompt and not ss.processing:
    ss.submitted_prompt = url_prompt
    ss.processing = True
    ss.prompt_source = "url"
    ss.consumed_url_prompt = True

# ---------- If a prompt is waiting, handle it NOW ----------
if ss.submitted_prompt and ss.processing:
    echo = (ss.prompt_source == "chat")  # ONLY chat_input echoes
    process_user_prompt(ss.submitted_prompt, echo_user=echo)

# ---------- Chat input LAST ----------
def on_submit():
    ss.submitted_prompt = ss.user_input
    ss.processing = True
    ss.prompt_source = "chat"

if ss.processing:
    st.chat_input(placeholder, disabled=True)
else:
    _ = st.chat_input(
        placeholder,
        key="user_input",
        on_submit=on_submit
    )