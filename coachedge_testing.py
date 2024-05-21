import openai
import streamlit as st
from openai import OpenAI
import uuid

client = OpenAI()

st.set_page_config(page_title="Coach Edge - Virtual Life Coach",layout="wide")

# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;} 
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.html(hide_st_style)

# st.html("""
#     <style>
#            .block-container {
#                 padding-top: 1rem;
#                 padding-left: 1rem;
#                 padding-right: 1rem;
#             }
#     </style>
#     """)

# Initialize session state variables
if "session_id" not in st.session_state:
   st.session_state.session_id = str(uuid.uuid4())
if "run" not in st.session_state:
   st.session_state.run = {"status": None}
if "messages" not in st.session_state:
   st.session_state.messages = []
if "retry_error" not in st.session_state:
   st.session_state.retry_error = 0
if 'prompt' not in st.session_state:
   st.session_state.prompt = ''
if 'input_count' not in st.session_state:
   st.session_state.input_count = 0
if "assistant" not in st.session_state:
   openai.api_key = st.secrets["OPENAI_API_KEY"]
   st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])
   st.session_state.thread = client.beta.threads.create()
#       metadata={'session_id': st.session_state.session_id}
 #  )

#Retrieve URL Parameters
Fname = st.query_params.get("fname", "Unknown")
School = st.query_params.get("school", "Unknown")
Team = st.query_params.get("team", "Unknown")
Role = st.query_params.get("role", "Unknown")
Language=st.query_params.get("language","Unknown")
additional_instructions = f"The users name is {Fname}. They are a {Role} on the {Team} team at {School}."

st.markdown("**Ask a question below or select a conversation starter**")    

button_prompt1 = 'How do I overcome phone anxiety when I get an unsolicited call from a dreaded customer?'
button_prompt2 = 'How do I keep money and success from becoming an idol?'
button_prompt3 = 'How to align passions with professional goals for fulfillment?'
button_prompt4 = 'How can I promote positive mental health and prevent burnout?'
button_prompt5 = 'How can I stay patient during the tough process of building my client base?'
button_prompt6 = 'How can I overcome the insecurity I feel by being younger than all of my clients?'

with st.expander("Conversation Starters"):
   # Create Predefine prompt buttons
   if st.button(button_prompt1):
        st.session_state.prompt = button_prompt1

   if st.button(button_prompt2):
        st.session_state.prompt = button_prompt2

   if st.button(button_prompt3):
        st.session_state.prompt = button_prompt3

   if st.button(button_prompt4):
        st.session_state.prompt = button_prompt4

   if st.button(button_prompt5):
        st.session_state.prompt = button_prompt5

   if st.button(button_prompt6):
        st.session_state.prompt = button_prompt6

typed_input = st.chat_input("What questions or thoughts are on your mind?")

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
 
                 