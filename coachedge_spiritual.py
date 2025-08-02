import streamlit as st

def main():
    st.title("Download the Latest Season Builder App")
    st.write("Get the latest version of the Season Builder App on your mobile device using the links below:")

    # Create two columns to display the links side-by-side.
    col1, col2 = st.columns(2)

    with col1:
        # Hyperlinked text for the Apple App Store
        st.markdown("[Download on the App Store](https://apps.apple.com/us/app/coach-edge/id6505067739)")
    
    with col2:
        # Hyperlinked text for the Google Play Store
        st.markdown("[Get it on Google Play](https://play.google.com/store/apps/details?id=com.coachedge.android)")

if __name__ == "__main__":
    main()    

# import openai
# import os
# import io
# import requests
# import streamlit as st
# from openai import OpenAI
# from translations_spiritual import translations

# # -----------------------------
# # Constants for avatar URLs
# # -----------------------------
# USER_AVATAR = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
# ASSISTANT_AVATAR = "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"

# # -----------------------------
# # Initialize OpenAI client
# # -----------------------------
# client = OpenAI()

# st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# # -----------------------------
# # Initialize session state with defaults
# # -----------------------------
# defaults = {
#     "messages": [],
#     "prompt": "",             
#     "submitted_prompt": "",   
#     "fname": "",
#     "school": "",
#     "team": "",
#     "role": "",
#     "language": "",
#     "processing": False,     
#     "thread": None,           
#     "assistant": None,        
#     "last_assistant_response": "",   # To store TTS-able text

#     # === NEW FOR AUTOPLAY ===
#     "audio_played": False,       # Tracks if we've already auto-played for this response
#     "audio_bytesio": None,       # Stores most recent audio
# }
# for key, default in defaults.items():
#     st.session_state.setdefault(key, default)

# # -----------------------------
# # Streamed TTS, output as BytesIO (no disk files, user/session safe)
# # -----------------------------
# def generate_speech_streaming(text, voice="alloy"):
#     if not text or not text.strip():
#         return None
#     buffer = io.BytesIO()
#     with client.audio.speech.with_streaming_response.create(
#         model="tts-1",
#         input=text,
#         voice=voice
#     ) as response:
#         for chunk in response.iter_bytes():
#             buffer.write(chunk)
#     buffer.seek(0)
#     return buffer

# # -----------------------------
# # Adalo Integration Functions
# # -----------------------------
# def update_adalo_user_thread(email, thread_id):
#     ADALO_APP_ID = os.getenv("APP_ID")
#     ADALO_COLLECTION_ID = os.getenv("ADALO_COLLECTION_ID")
#     ADALO_API_KEY = os.getenv("ADALO_API_KEY")
#     headers = {
#         "Authorization": f"Bearer {ADALO_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     get_url = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}?filterKey=Email&filterValue={email}"
#     response = requests.get(get_url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         if data.get("records") and len(data["records"]) > 0:
#             record = data["records"][0]
#             element_id = record.get("id")  
#             update_url = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}/{element_id}"
#             payload = {"thread_id": thread_id}
#             update_response = requests.put(update_url, json=payload, headers=headers)
#             if update_response.status_code != 200:
#                 st.write("DEBUG: Failed to update Adalo record:", update_response.text)

# # -----------------------------
# # OpenAI Thread Handling
# # -----------------------------
# def initialize_openai_assistant():
#     if not st.session_state.assistant:
#         openai.api_key = os.getenv("OPENAI_API_KEY")
#         st.session_state.assistant = openai.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT"))

# def handle_thread():
#     params = st.query_params
#     if "thread_id" in params and params["thread_id"]:
#         thread_id = params["thread_id"]
#         st.session_state.thread = openai.beta.threads.retrieve(thread_id)
#     else:
#         new_thread = client.beta.threads.create()
#         st.session_state.thread = new_thread
#         email = params.get("email", "")
#         if email:
#             update_adalo_user_thread(email, new_thread.id)

# def get_url_parameters():
#     params = st.query_params
#     st.session_state.fname = params.get("fname", "Unknown")
#     st.session_state.school = params.get("school", "Unknown")
#     st.session_state.team = params.get("team", "Unknown")
#     st.session_state.role = params.get("role", "Unknown")
#     st.session_state.language = params.get("language", "Unknown")
#     st.session_state.prompt = params.get("prompt", "")

# def extract_language(lang_str):
#     parts = lang_str.split('(')
#     if len(parts) > 1:
#         return parts[1].split(')')[0]
#     return "Unknown"

# # -----------------------------
# # Chat and Message Functions
# # -----------------------------
# def display_chat_messages():
#     for message in st.session_state.messages:
#         role = message["role"]
#         avatar = USER_AVATAR if role == "user" else ASSISTANT_AVATAR
#         with st.chat_message(role, avatar=avatar):
#             st.markdown(message["content"])

# def process_user_prompt(prompt, additional_instructions):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user", avatar=USER_AVATAR):
#         st.markdown(prompt)
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
#     st.session_state.last_assistant_response = final_response  # Save for TTS

#     # === NEW: Reset audio flags for new assistant reply ===
#     st.session_state.audio_played = False
#     st.session_state.audio_bytesio = None

#     st.session_state.submitted_prompt = ""
#     st.session_state.processing = False
#     st.rerun()

# def chat_submit_callback():
#     st.session_state.submitted_prompt = st.session_state.user_input
#     st.session_state.processing = True

# # -----------------------------
# # Main Execution Flow
# # -----------------------------
# initialize_openai_assistant()
# get_url_parameters()
# handle_thread()

# lang = extract_language(st.session_state.language)
# lang_translations = translations.get(lang, translations["English"])

# st.markdown(lang_translations["ask_question"])

# with st.expander(lang_translations["expander_title"]):
#     for idx, button_text in enumerate(lang_translations["button_prompts"]):
#         if st.button(button_text):
#             st.session_state.submitted_prompt = lang_translations["prompts"][idx]
#             st.session_state.processing = True

# display_chat_messages()

# if st.session_state.processing:
#     st.chat_input(lang_translations["typed_input_placeholder"], disabled=True)
# else:
#     _ = st.chat_input(
#         lang_translations["typed_input_placeholder"],
#         key="user_input",
#         on_submit=chat_submit_callback
#     )

# # --- AUTOPLAY + "LISTEN AGAIN" BUTTON BELOW – replaces your old Listen button section ---
# if st.session_state.last_assistant_response:
#     if not st.session_state.audio_played:
#         # Autoplay: generate TTS audio, play, cache for replay
#         audio_bytesio = generate_speech_streaming(st.session_state.last_assistant_response)
#         if audio_bytesio:
#             st.audio(audio_bytesio, format="audio/mp3")
#             st.session_state.audio_bytesio = audio_bytesio
#             st.session_state.audio_played = True
#         else:
#             st.warning("Audio generation failed.")
#     else:
#         # Allow replay
#         if st.button("🔊 Listen again"):
#             audio_bytesio = st.session_state.audio_bytesio
#             if audio_bytesio:
#                 st.audio(audio_bytesio, format="audio/mp3")
#             else:
#                 st.warning("Audio not found.")

# if st.session_state.submitted_prompt and st.session_state.processing:
#     additional_instructions = (
#         f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of "
#         f"{st.session_state.team} at the {st.session_state.school}. Please note that their native language is "
#         f"{st.session_state.language}. THIS IS IMPORTANT ... When I ask a question or provide a response, please "
#         f"respond in their native language regardless of the language they use to ask the question or provide a response. "
#         f"Pay special attention not to accidentally use words from another language when providing a response."
#     )
#     process_user_prompt(st.session_state.submitted_prompt, additional_instructions)                                                                                                                                                                                                                                                                                                                                       