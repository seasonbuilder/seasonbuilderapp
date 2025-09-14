# import os
# import streamlit as st
# from openai import OpenAI

# # ---------- Page config ----------
# st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# # ---------- Cache heavy/static things ----------

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# assistant = client.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))

# # ---------- Session state ----------
# defaults = {
#     "messages": [],
#     "prompt": "",
#     "fname": "",
#     "school": "",
#     "team": "",
#     "role": "",
#     "language": "",
#     "thread_id": None,            # use ID only; no need to retrieve the object
#     "consumed_url_prompt": False  # consume ?prompt= only once
# }
# for k, v in defaults.items():
#     st.session_state.setdefault(k, v)

# # ---------- URL parameters ----------
# params = st.query_params
# st.session_state.fname = params.get("fname", st.session_state.fname or "Unknown")
# st.session_state.school = params.get("school", st.session_state.school or "Unknown")
# st.session_state.team = params.get("team", st.session_state.team or "Unknown")
# st.session_state.role = params.get("role", st.session_state.role or "Unknown")
# st.session_state.language = params.get("language", st.session_state.language or "Unknown")

# url_thread_id = params.get("thread_id", None)
# if url_thread_id and st.session_state.thread_id != url_thread_id:
#     st.session_state.thread_id = url_thread_id

# # Create a thread exactly once if we still don't have one
# if not st.session_state.thread_id:
#     st.session_state.thread_id = client.beta.threads.create().id

# # Optional URL prompt (consume once so it doesn’t repeat on reruns)
# url_prompt = params.get("prompt", None)
# if url_prompt and not st.session_state.consumed_url_prompt:
#     st.session_state.prompt = url_prompt
#     st.session_state.consumed_url_prompt = True

# # ---------- Language helpers ----------
# def extract_language(lang_str: str) -> str:
#     parts = lang_str.split("(")
#     return parts[1].split(")")[0] if len(parts) > 1 else "Unknown"

# lang_label = extract_language(st.session_state.language)


# # ---------- Chat input ----------
# typed_input = st.chat_input()
# if typed_input:
#     st.session_state.prompt = typed_input

# # ---------- Show last N messages to keep UI fast ----------
# MAX_UI_MESSAGES = 30
# for msg in st.session_state.messages[-MAX_UI_MESSAGES:]:
#     role = msg["role"]
#     avatar = (
#         "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
#         if role == "user"
#         else "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"
#     )
#     with st.chat_message(role, avatar=avatar):
#         st.markdown(msg["content"])

# # ---------- Process a new prompt ----------
# if st.session_state.prompt:
#     user_text = st.session_state.prompt

#     # Add to UI history
#     st.session_state.messages.append({"role": "user", "content": user_text})
#     with st.chat_message("user", avatar="https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"):
#         st.markdown("Thinking ...")

#     # Add to thread (no retrieve needed)
#     client.beta.threads.messages.create(
#         thread_id=st.session_state.thread_id,
#         role="user",
#         content=user_text,
#     )

#     # Keep per-turn instructions short (put heavy policy in Assistant config)
#     addl = (
#         f"User name: {st.session_state.fname}. Role: {st.session_state.role}. "
#         f"Team: {st.session_state.team}. School: {st.session_state.school}. "
#         f"Native language: {lang_label}. If native language is 'Unknown', use English. "
#         f"Always respond in the user's native language regardless of the language used in their message."
#     )

#     # Stream response with light throttling
#     chunks, tick = [], 0
#     with st.chat_message("assistant", avatar="https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"):
#         container = st.empty()
#         try:
#             stream = client.beta.threads.runs.create(
#                 assistant_id=assistant.id,
#                 thread_id=st.session_state.thread_id,
#                 additional_instructions=addl,
#                 stream=True,
#             )
#             if stream:
#                 for event in stream:
#                     if event.data.object == "thread.message.delta":
#                         for c in event.data.delta.content:
#                             if c.type == "text":
#                                 chunks.append(c.text.value)
#                                 tick += 1
#                                 if tick % 8 == 0:  # fewer DOM writes
#                                     container.markdown("".join(chunks).strip())
#         except Exception as e:
#             chunks.append(f"\n\n_(Sorry, something went wrong: {e})_")

#         # final flush
#         assistant_text = "".join(chunks).strip() or "_(No response.)_"
#         container.markdown(assistant_text)

#     st.session_state.messages.append({"role": "assistant", "content": assistant_text})
#     st.session_state.prompt = ""
import os
import streamlit as st
from openai import OpenAI

# ---------- Page config ----------
st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# ---------- OpenAI client ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PROMPT_ID = os.getenv("OPENAI_PROMPT_ID")  # e.g., "prompt_abc123"

# ---------- Session state ----------
defaults = {
    "messages": [],
    "prompt": "",
    "fname": "",
    "school": "",
    "team": "",
    "role": "",
    "language": "",
    "conversation_id": None,        # replaces thread_id
    "consumed_url_prompt": False,   # consume ?prompt= once
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)
ss = st.session_state

# ---------- URL parameters ----------
params = st.query_params
ss.fname    = params.get("fname",    ss.fname or "Unknown")
ss.school   = params.get("school",   ss.school or "Unknown")
ss.team     = params.get("team",     ss.team or "Unknown")
ss.role     = params.get("role",     ss.role or "Unknown")
ss.language = params.get("language", ss.language or "Unknown")

# Resume conversation if provided
url_convo_id = params.get("conversation_id")
if url_convo_id and ss.conversation_id != url_convo_id:
    ss.conversation_id = url_convo_id

# Create a conversation once if we still don't have one
if not ss.conversation_id:
    conv = client.conversations.create()
    ss.conversation_id = conv.id

# Optional URL prompt (consume once so it doesn’t repeat on reruns)
url_prompt = params.get("prompt")
if url_prompt and not ss.consumed_url_prompt:
    ss.prompt = url_prompt
    ss.consumed_url_prompt = True

# ---------- Helpers ----------
USER_AVATAR = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
ASSISTANT_AVATAR = "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"

def extract_language(label: str) -> str:
    parts = label.split("(")
    return parts[1].split(")")[0] if len(parts) > 1 else "Unknown"

lang_label = extract_language(ss.language)

# ---------- Chat input ----------
typed_input = st.chat_input()
if typed_input:
    ss.prompt = typed_input

# ---------- Show recent messages ----------
MAX_UI_MESSAGES = 30
for m in ss.messages[-MAX_UI_MESSAGES:]:
    avatar = USER_AVATAR if m["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

# ---------- Process a new prompt (Prompt reference + per-turn system context) ----------
if ss.prompt:
    user_text = ss.prompt

    # Echo user message
    ss.messages.append({"role": "user", "content": user_text})
#    with st.chat_message("user", avatar=USER_AVATAR):
#        st.markdown(user_text)

    # Build input items:
    # 1) A small SYSTEM item with dynamic context for this user/turn
    # 2) The USER item with the actual question
    system_context = (
        f"User name: {ss.fname}. "
        f"Role: {ss.role}. Team: {ss.team}. School: {ss.school}. "
        f"Native language: {lang_label}. "
        f"Always respond in the user's native language; if 'Unknown', use English. "
        f"Do not mix languages inadvertently."
    )
    input_items = [
        {"role": "system", "content": system_context},
        {"role": "user",   "content": user_text},
    ]

    # Stream response (prompt points to your Chat Prompt; no model/instructions inline)
    chunks, tick = [], 0
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        container = st.empty()
        try:
            stream = client.responses.create(
                prompt={"id": PROMPT_ID},          # Use your Chat Prompt (defines model/tools/instructions)
                conversation=ss.conversation_id,   # Keep context
                input=input_items,                 # Per-turn system + user
                stream=True
            )
            for event in stream:
                # Canonical text delta event
                if getattr(event, "type", "") == "response.output_text.delta":
                    chunks.append(event.delta)
                    tick += 1
                    if tick % 8 == 0:             # throttle DOM writes
                        container.markdown("".join(chunks).strip())
        except Exception as e:
            chunks.append(f"\n\n_(Sorry, something went wrong: {e})_")

        # Final flush
        assistant_text = "".join(chunks).strip() or "_(No response.)_"
        container.markdown(assistant_text)

    ss.messages.append({"role": "assistant", "content": assistant_text})
    ss.prompt = ""