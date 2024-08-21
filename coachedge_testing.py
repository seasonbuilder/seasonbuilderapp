import openai
import streamlit as st
from openai import OpenAI
import uuid

client = OpenAI()

st.set_page_config(page_title="Coach Edge - Virtual Life Coach",page_icon="https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png", layout="wide")

if "messages" not in st.session_state:
   st.session_state.messages = []

if 'prompt' not in st.session_state:
   st.session_state.prompt = ''
   
if "assistant" not in st.session_state:
   openai.api_key = st.secrets["OPENAI_API_KEY"]
   st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])
   st.session_state.thread = client.beta.threads.create()

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


#Retrieve URL Parameters
st.session_state.fname = st.query_params.get("fname", "Unknown")
st.session_state.school = st.query_params.get("school", "Unknown")
st.session_state.team = st.query_params.get("team", "Unknown")
st.session_state.role = st.query_params.get("role", "Unknown")
st.session_state.language=st.query_params.get("language","Unknown")
st.session_state.prompt=st.query_params.get("prompt")

additional_instructions = f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} on the {st.session_state.team} team at the {st.session_state.school} and their native language is {st.session_state.language}. If the response is not given to them in their native language, give a response in their native language too."

# st.markdown("**Ask a question below or select a conversation starter**")    

# button_prompt1 = 'How can I be a better Christian example to my team?'
# button_prompt2 = 'How do I better align with my Christian identity'
# button_prompt3 = 'What are 5 scriptures that help me stay positive and resilient'
# button_prompt4 = 'What do I do if I don’t know God’s purpose for my life?'
# button_prompt5 = 'How can I be a servant leader?'
# button_prompt6 = 'What does Ephesians 2:10 mean and how does that apply to me?'

# with st.expander("Conversation Starters"):
#    # Create Predefine prompt buttons
#    if st.button(button_prompt1):
#         st.session_state.prompt = button_prompt1

#    if st.button(button_prompt2):
#         st.session_state.prompt = button_prompt2

#    if st.button(button_prompt3):
#         st.session_state.prompt = button_prompt3

#    if st.button(button_prompt4):
#         st.session_state.prompt = button_prompt4

#    if st.button(button_prompt5):
#         st.session_state.prompt = button_prompt5

#    if st.button(button_prompt6):
#         st.session_state.prompt = button_prompt6

typed_input = st.chat_input("What's on your mind?")

if typed_input:
    st.session_state.prompt = typed_input

for message in st.session_state.messages:
    if message["role"] == "user":
       with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
          st.markdown(message["content"])
    else:
       with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
          st.markdown(message["content"])

# Check if there is typed input
if st.session_state.prompt:
    delta = [] 
    response = ""
    st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
    with st.chat_message('user',avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
        st.markdown(st.session_state.prompt)
    with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
        container = st.empty()
        st.session_state.thread_messages= client.beta.threads.messages.create(
              st.session_state.thread.id, role="user",content=st.session_state.prompt
        )

        stream = client.beta.threads.runs.create(
            assistant_id=st.session_state.assistant.id,
            thread_id = st.session_state.thread.id,
            additional_instructions = additional_instructions,
            stream = True
        )
        if stream:
           for event in stream:
              if event.data.object == "thread.message.delta":
                 for content in event.data.delta.content:
                    if content.type == 'text':
                       delta.append(content.text.value)
                       response = "".join(item for item in delta if item).strip()
                       container.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
                                  