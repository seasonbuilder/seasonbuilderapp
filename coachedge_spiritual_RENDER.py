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

# # Responses API currently still requires `model` in many setups
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

# # ---------- URL parameters (backward compatible; adds program= only) ----------
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

# # Resume ONLY if conversation_id is provided and non-blank.
# # Your URL will always include conversation_id=, but it may be blank.
# passed_convo_id = (qp.get("conversation_id") or "").strip() or None
# if passed_convo_id and ss.conversation_id != passed_convo_id:
#     ss.conversation_id = passed_convo_id

# # ---------- Helpers ----------
# def is_athlete_role(role_value: str) -> bool:
#     return (role_value or "").strip().lower() == "athlete"

# def extract_language(label: str) -> str:
#     parts = (label or "").split("(")
#     return parts[1].split(")")[0].strip() if len(parts) > 1 else "Unknown"

# def t_for(lang_label: str) -> dict:
#     return LANGS.get(lang_label, LANGS.get("English", {}))

# def tkey(lang_dict: dict, key: str, default: str) -> str:
#     return lang_dict.get(key, default)

# lang_label = extract_language(ss.language)
# LANG = t_for(lang_label)

# # If ?prompt= is passed, we will NOT use the translations UI.
# url_prompt = qp.get("prompt")
# use_translations_ui = not bool(url_prompt)

# if use_translations_ui:
#     ask_q = tkey(LANG, "ask_question", "### **Ask Coach Edge**")
#     expander_title = tkey(LANG, "expander_title", "Topics To Get You Started")
#     button_prompts = LANG.get("button_prompts", [])
#     button_prompt_vals = LANG.get("prompts", [])
#     placeholder = tkey(LANG, "typed_input_placeholder", "How else can I help?")
# else:
#     # Minimal UI when processing a URL prompt
#     ask_q = ""
#     expander_title = ""
#     button_prompts = []
#     button_prompt_vals = []
#     placeholder = "How else can I help?"

# # ---------- Adalo sync (only when we create a new conversation; NEVER for athletes) ----------
# def update_adalo_user_conversation_once(email_: str, conversation_id_: str):
#     # Hard stop for athletes (your requirement)
#     if is_athlete_role(ss.role):
#         return
#     if not email_ or not conversation_id_ or ss.adalo_synced:
#         return

#     app_id = os.getenv("APP_ID")
#     col_id = os.getenv("ADALO_COLLECTION_ID")
#     api_key = os.getenv("ADALO_API_KEY")
#     if not (app_id and col_id and api_key):
#         return

#     headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
#     base = f"https://api.adalo.com/v0/apps/{app_id}/collections/{col_id}"

#     # Assumes you created a column named conversation_id in Adalo Users
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
#     """
#     1) If URL provides a usable conversation_id, use it (no creation, no Adalo write).
#     2) Else if we already have one in session, keep it.
#     3) Else create a new conversation.
#        - Only sync to Adalo if NOT athlete.
#     """
#     if ss.conversation_id:
#         return

#     conv = client.conversations.create()
#     ss.conversation_id = conv.id

#     # NEVER store conversation_id for athletes
#     if not is_athlete_role(ss.role):
#         update_adalo_user_conversation_once(email, conv.id)

# ensure_conversation()

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
#     # Only echo if it came from chat_input (your requirement)
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
#                 #model=OPENAI_MODEL,
#                 prompt={"id": PROMPT_ID},
#                 conversation=ss.conversation_id,
#                 input=input_items,
#                 stream=True,
#                 store=True,
#             )
#             for event in stream:
#                 if getattr(event, "type", "") == "response.output_text.delta":
#                     chunks.append(event.delta)
#                     tick += 1
#                     if tick % 8 == 0:
#                         container.markdown("".join(chunks).strip())
#         except Exception as e:
#             chunks.append(f"\n\n_(Sorry, something went wrong: {e})_")

#         assistant_text = "".join(chunks).strip() or "_(No response.)_"
#         container.markdown(assistant_text)

#     ss.messages.append({"role": "assistant", "content": assistant_text})

#     # Clear flags so input enables on this render pass
#     ss.submitted_prompt = ""
#     ss.processing = False
#     ss.prompt_source = ""

# # =========================================================
# # UI ORDER (fixes the "echo above expander" and "no response" issues):
# # 1) header/buttons
# # 2) history
# # 3) queue URL prompt once (no echo)
# # 4) process queued prompt (renders assistant reply in-place)
# # 5) chat_input last
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
import html
import requests
import streamlit as st
from openai import OpenAI
from translations_spiritual_new import translations as T  # external translations

# ---------- Page config ----------
st.set_page_config(
    page_title="Coach Edge",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Constants ----------
PRIMARY = "#003462"
PRIMARY_DARK = "#002847"
GOLD = "#f3e368"
GOLD_DEEP = "#e4c33a"
SOFT_BG = "#f6f8fb"
TEXT = "#162033"
MUTED = "#667085"

USER_AVATAR = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
ASSISTANT_AVATAR = "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"
MAX_UI_MESSAGES = 30

# Optional: set these in Render if you want the branded images to appear.
# COACH_EDGE_PHOTO_URL should be a square/circle-friendly headshot.
# MOUNTAIN_IMAGE_URL should be your 4x3 mountain image, ideally blended to #003463.
COACH_EDGE_PHOTO_URL = os.getenv("COACH_EDGE_PHOTO_URL", ASSISTANT_AVATAR)
MOUNTAIN_IMAGE_URL = os.getenv("MOUNTAIN_IMAGE_URL", "")

# ---------- Prompt routing (SB / CB) ----------
PROMPT_ID_SB = os.getenv("OPENAI_PROMPT_ID_SB") or os.getenv("OPENAI_PROMPT_ID")
PROMPT_ID_CB = os.getenv("OPENAI_PROMPT_ID_CB") or os.getenv("OPENAI_PROMPT_ID")
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
ss.setdefault("submitted_prompt", "")
ss.setdefault("processing", False)
ss.setdefault("prompt_source", "")  # "chat" | "url" | "button"
ss.setdefault("consumed_url_prompt", False)
ss.setdefault("conversation_id", None)
ss.setdefault("adalo_synced", False)

# ---------- URL parameters ----------
qp = st.query_params
ss.fname = qp.get("fname", ss.fname or "")
ss.school = qp.get("school", ss.school or "")
ss.team = qp.get("team", ss.team or "")
ss.role = qp.get("role", ss.role or "")
ss.language = qp.get("language", ss.language or "")

email = qp.get("email") or ""
program = (qp.get("program") or "SB").strip().upper()
if program not in ("SB", "CB"):
    program = "SB"
PROMPT_ID = PROMPT_ID_SB if program == "SB" else PROMPT_ID_CB

passed_convo_id = (qp.get("conversation_id") or "").strip() or None
if passed_convo_id and ss.conversation_id != passed_convo_id:
    ss.conversation_id = passed_convo_id

# ---------- Helpers ----------
def is_athlete_role(role_value: str) -> bool:
    return (role_value or "").strip().lower() == "athlete"

def safe_text(value: str, fallback: str = "") -> str:
    value = (value or "").strip()
    return value if value and value.lower() != "unknown" else fallback

def extract_language(label: str) -> str:
    parts = (label or "").split("(")
    return parts[1].split(")")[0].strip() if len(parts) > 1 else "Unknown"

def t_for(lang_label: str) -> dict:
    return LANGS.get(lang_label, LANGS.get("English", {}))

def tkey(lang_dict: dict, key: str, default: str) -> str:
    return lang_dict.get(key, default)

def queue_prompt(prompt_text: str, source: str = "button"):
    if not ss.processing and prompt_text:
        ss.submitted_prompt = prompt_text
        ss.processing = True
        ss.prompt_source = source

lang_label = extract_language(ss.language)
LANG = t_for(lang_label)
url_prompt = qp.get("prompt")
use_translations_ui = not bool(url_prompt)

if use_translations_ui:
    expander_title = tkey(LANG, "expander_title", "Topics To Get You Started")
    button_prompts = LANG.get("button_prompts", [])
    button_prompt_vals = LANG.get("prompts", [])
    placeholder = tkey(LANG, "typed_input_placeholder", "What's on your mind?")
else:
    expander_title = ""
    button_prompts = []
    button_prompt_vals = []
    placeholder = "What's on your mind?"

first_name = safe_text(ss.fname, "there")
team = safe_text(ss.team)
school = safe_text(ss.school)
role = safe_text(ss.role)

# ---------- Styling ----------
def inject_css():
    mountain_rule = ""
    if MOUNTAIN_IMAGE_URL:
        mountain_rule = f"background-image: linear-gradient(90deg, rgba(0,52,98,.97) 0%, rgba(0,52,98,.88) 48%, rgba(0,52,98,.45) 100%), url('{MOUNTAIN_IMAGE_URL}');"
    else:
        mountain_rule = "background: radial-gradient(circle at 80% 20%, #0b5a92 0%, #003462 38%, #002847 100%);"

    st.markdown(
        f"""
        <style>
            :root {{
                --primary: {PRIMARY};
                --primary-dark: {PRIMARY_DARK};
                --gold: {GOLD};
                --gold-deep: {GOLD_DEEP};
                --soft-bg: {SOFT_BG};
                --text: {TEXT};
                --muted: {MUTED};
            }}

            html, body, [data-testid="stAppViewContainer"] {{
                background: var(--soft-bg);
            }}

            [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {{
                visibility: hidden;
                height: 0;
            }}

            .block-container {{
                max-width: 430px !important;
                padding: 0 14px 56px 14px !important;
                margin: 0 auto !important;
            }}

            .coach-hero {{
                {mountain_rule}
                background-size: cover;
                background-position: center right;
                color: white;
                border-radius: 0 0 22px 22px;
                margin: -12px -14px 16px -14px;
                padding: 26px 18px 22px 18px;
                box-shadow: 0 8px 24px rgba(0, 52, 98, .22);
            }}

            .hero-topline {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
            }}

            .hero-kicker {{
                color: var(--gold);
                font-size: 12px;
                font-weight: 800;
                letter-spacing: .13em;
                text-transform: uppercase;
                margin-bottom: 8px;
            }}

            .hero-title {{
                font-size: 25px;
                line-height: 1.12;
                font-weight: 850;
                margin: 0 0 8px 0;
            }}

            .hero-subtitle {{
                font-size: 15px;
                line-height: 1.42;
                opacity: .94;
                max-width: 330px;
                margin: 0;
            }}

            .coach-avatar {{
                width: 56px;
                height: 56px;
                border-radius: 50%;
                object-fit: cover;
                border: 3px solid var(--gold);
                box-shadow: 0 5px 16px rgba(0,0,0,.25);
                flex: 0 0 auto;
            }}

            .section-label {{
                font-size: 13px;
                font-weight: 850;
                letter-spacing: .04em;
                color: var(--primary);
                margin: 18px 0 8px 2px;
                text-transform: uppercase;
            }}

            .coach-card {{
                background: white;
                border: 1px solid rgba(0, 52, 98, .08);
                border-radius: 18px;
                padding: 15px;
                box-shadow: 0 7px 20px rgba(16, 24, 40, .07);
                margin-bottom: 14px;
            }}

            .thought-card {{
                background: linear-gradient(135deg, #ffffff 0%, #fffdf2 100%);
                border-left: 5px solid var(--gold);
            }}

            .thought-kicker {{
                color: var(--primary);
                font-size: 12px;
                font-weight: 850;
                letter-spacing: .08em;
                text-transform: uppercase;
                margin-bottom: 6px;
            }}

            .thought-text {{
                color: var(--text);
                font-size: 17px;
                line-height: 1.36;
                font-weight: 720;
                margin: 0;
            }}

            .profile-card {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}

            .profile-card img {{
                width: 52px;
                height: 52px;
                border-radius: 50%;
                object-fit: cover;
                border: 2px solid var(--gold);
            }}

            .profile-title {{
                color: var(--primary);
                font-weight: 850;
                font-size: 16px;
                margin-bottom: 2px;
            }}

            .profile-copy {{
                color: var(--muted);
                font-size: 13px;
                line-height: 1.35;
            }}

            .topics-wrap {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
                margin-bottom: 4px;
            }}

            div.stButton > button {{
                width: 100%;
                min-height: 42px;
                border-radius: 14px;
                border: 1px solid rgba(0, 52, 98, .13);
                background: #fff;
                color: var(--primary);
                font-weight: 750;
                font-size: 13px;
                box-shadow: 0 3px 10px rgba(16, 24, 40, .05);
                white-space: normal;
                text-align: center;
            }}

            div.stButton > button:hover {{
                border-color: var(--primary);
                background: #f1f6fb;
                color: var(--primary);
            }}

            .hint-card {{
                background: #edf5fb;
                border-radius: 16px;
                padding: 13px 14px;
                color: var(--primary);
                font-size: 13px;
                line-height: 1.4;
                margin: 8px 0 12px 0;
            }}

            .hint-card strong {{
                color: var(--primary);
            }}

            [data-testid="stChatMessage"] {{
                background: white;
                border-radius: 18px;
                padding: 10px 12px;
                margin: 10px 0;
                box-shadow: 0 4px 16px rgba(16, 24, 40, .06);
                border: 1px solid rgba(0, 52, 98, .08);
            }}

            [data-testid="stChatMessage"] p {{
                font-size: 15px;
                line-height: 1.46;
            }}

            [data-testid="stChatInput"] {{
                max-width: 430px;
                margin: 0 auto;
            }}
    

            [data-testid="stChatInput"] > div {{
                align-items: center !important;
            }}

            [data-testid="stChatInput"] button {{
                position: absolute !important;
                right: 12px !important;
                bottom: 10px !important;
                width: 34px !important;
                height: 34px !important;
                min-height: 34px !important;
                border-radius: 12px !important;
            }}

            [data-testid="stChatInput"] textarea {{
                border-radius: 18px !important;
                padding: 12px 46px 12px 18px !important;
                border: 1px solid rgba(0, 52, 98, .12) !important;
                min-height: 46px !important;
                height: 46px !important;
                line-height: 20px !important;
            }}

            .small-divider {{
                height: 1px;
                background: rgba(0,52,98,.10);
                margin: 16px 0 6px 0;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()

# ---------- Adalo sync ----------
def update_adalo_user_conversation_once(email_: str, conversation_id_: str):
    # Never store conversation_id for athletes.
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
    payload = {"conversation_id": conversation_id_}

    try:
        r = http.get(f"{base}?filterKey=Email&filterValue={email_}", headers=headers, timeout=10)
        if r.status_code != 200:
            return
        records = (r.json() or {}).get("records") or []
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
    if not is_athlete_role(ss.role):
        update_adalo_user_conversation_once(email, conv.id)

ensure_conversation()

# ---------- System context ----------
def build_system_context() -> str:
    return (
        f"User name: {ss.fname or 'Unknown'}. "
        f"Role: {ss.role or 'Unknown'}. Team: {ss.team or 'Unknown'}. School: {ss.school or 'Unknown'}. "
        f"Native language: {lang_label}. "
        f"Program: {program}. "
        f"Always respond in the user's native language; if 'Unknown', use English. "
        f"Do not mix languages inadvertently."
    )

# ---------- Processing ----------
def process_user_prompt(prompt_text: str, echo_user: bool):
    if echo_user:
        ss.messages.append({"role": "user", "content": prompt_text})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt_text)

    input_items = [
        {"role": "system", "content": build_system_context()},
        {"role": "user", "content": prompt_text},
    ]

    chunks, tick = [], 0
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        container = st.empty()
        try:
            stream = client.responses.create(
                prompt={"id": PROMPT_ID},
                conversation=ss.conversation_id,
                input=input_items,
                stream=True,
                store=True,
            )
            for event in stream:
                if getattr(event, "type", "") == "response.output_text.delta":
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

# ---------- Branded landing UI ----------
def render_landing():
    escaped_name = html.escape(first_name)
    hero_kicker = html.escape(tkey(LANG, "coach_hero_kicker", "Coach Edge"))
    hero_title_template = tkey(LANG, "coach_hero_title", "Hi {name} 👋")
    hero_title = html.escape(hero_title_template.format(name=first_name))
    hero_subtitle = html.escape(tkey(
        LANG,
        "coach_hero_subtitle",
        "I’m here to help you think through life, sport, faith, leadership, pressure, and the person you are becoming."
    ))
    popular_title = html.escape(tkey(LANG, "popular_topics_title", "Popular Topics"))
    topics_hint = html.escape(tkey(LANG, "topics_hint", "Tap a topic or type what is on your mind below."))

    st.markdown(
        f"""
        <div class="coach-hero">
            <div class="hero-topline">
                <div>
                    <div class="hero-kicker">{hero_kicker}</div>
                    <h1 class="hero-title">{hero_title}</h1>
                    <p class="hero-subtitle">{hero_subtitle}</p>
                </div>
                <img class="coach-avatar" src="{COACH_EDGE_PHOTO_URL}" alt="Coach Edge" />
            </div>
        </div>

        <div class="section-label">{popular_title}</div>
        <div class="hint-card">{topics_hint}</div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Topic prompt helpers ----------
def default_topics():
    # Used if translation topic prompts are not available.
    labels = [
        "🧠 Confidence",
        "😰 Anxiety",
        "🎯 Purpose",
        "👥 Leadership",
        "💬 Hard Conversations",
        "🙏 Faith",
        "🏆 Performance",
        "🤝 Relationships",
    ]
    prompts = [
        "I want to grow in confidence. Ask me a few questions and help me think through it.",
        "I am dealing with anxiety or pressure. Help me slow down and think clearly.",
        "Help me think about my purpose and the person I am becoming.",
        "I want to grow as a leader. Help me identify one practical step I can take.",
        "I need help preparing for a hard conversation.",
        "Help me think about this from a faith based perspective.",
        "Help me with my mindset around performance.",
        "I need help thinking through a relationship or teammate situation.",
    ]
    return labels, prompts

def render_topics():
    labels = list(LANG.get("popular_topic_labels") or button_prompts or [])
    prompts = list(LANG.get("popular_topic_prompts") or button_prompt_vals or [])

    if not labels or not prompts:
        labels, prompts = default_topics()

    # Keep the landing screen scannable. Full translated lists can still work,
    # but the first 8 are usually enough for the mobile view.
    max_topics = min(len(labels), len(prompts), 8)

    st.markdown('<div class="topics-wrap">', unsafe_allow_html=True)
    for idx in range(max_topics):
        if st.button(labels[idx], key=f"topic_{idx}", disabled=ss.processing):
            queue_prompt(prompts[idx], source="button")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- UI order ----------
# 1) landing/topics when no conversation yet
# 2) history
# 3) queue URL prompt once
# 4) process queued prompt
# 5) chat_input last

show_landing = use_translations_ui and len(ss.messages) == 0 and not ss.processing
if show_landing:
    render_landing()
    render_topics()
elif use_translations_ui and len(ss.messages) == 0:
    # While processing the first prompt, keep a small branded header visible.
    render_landing()

# ---------- Show last N messages ----------
if ss.messages:
    conversation_label = html.escape(tkey(LANG, "conversation_label", "Conversation"))
    st.markdown(f'<div class="section-label">{conversation_label}</div>', unsafe_allow_html=True)

for m in ss.messages[-MAX_UI_MESSAGES:]:
    avatar = USER_AVATAR if m["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

# ---------- Consume URL prompt once without echo ----------
if url_prompt and not ss.consumed_url_prompt and not ss.processing:
    ss.submitted_prompt = url_prompt
    ss.processing = True
    ss.prompt_source = "url"
    ss.consumed_url_prompt = True

# ---------- Process queued prompt after history ----------
if ss.submitted_prompt and ss.processing:
    echo = ss.prompt_source == "chat"
    process_user_prompt(ss.submitted_prompt, echo_user=echo)

# ---------- Chat input last ----------
def on_submit():
    ss.submitted_prompt = ss.user_input
    ss.processing = True
    ss.prompt_source = "chat"

if ss.processing:
    st.chat_input(placeholder, disabled=True)
else:
    st.chat_input(
        placeholder,
        key="user_input",
        on_submit=on_submit,
    )
