# import openai
# import time
# import datetime
# import uuid
# import streamlit as st
# from openai import OpenAI
 
# st.set_page_config(page_title="Coach Edge - Virtual Life Coach")

# # Function to update the run status (simulating the retrieval process)
# def update_run_status():
#     # Retrieving run status
#     st.session_state.run = client.beta.threads.runs.retrieve(
#         thread_id=st.session_state.thread.id,
#         run_id=st.session_state.run.id,
#     )
   
# def display_results():

#     # If run is completed, get messages
#     st.session_state.messages = client.beta.threads.messages.list(
#         thread_id=st.session_state.thread.id
#     )
#     for message in reversed(st.session_state.messages.data):
#         if message.role in ["user"]: 
#             with st.chat_message('user',avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#                 for content_part in message.content:
#                     message_text = content_part.text.value
#                     st.markdown(message_text)
#         elif message.role in ["assistant"]: 
#             with st.chat_message('assistant',avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#                 for content_part in message.content:
#                     message_text = content_part.text.value
#                     st.markdown(message_text)
                 

# # Initialize the client
# client = OpenAI()

# # Initialize session state variables

# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# if "run" not in st.session_state:
#     st.session_state.run = {"status": None}

# if "messages" not in st.session_state:
#    st.session_state.messages = []

# if "retry_error" not in st.session_state:
#    st.session_state.retry_error = 0

# if 'prompt' not in st.session_state:
#    st.session_state.prompt = ''

# if 'input_count' not in st.session_state:
#    st.session_state.input_count = 0

# #Retrieve URL Parameters
# Fname = st.query_params.get("fname", "Unknown")
# School = st.query_params.get("school", "Unknown")
# Team = st.query_params.get("team", "Unknown")
# Role = st.query_params.get("role", "Unknown")
# Language=st.query_params.get("language","Unknown")

# additional_instructions = f"The users name is {Fname}. They are a {Role} on the {Team} team at the {School}. Provide each response in 2 languages... 1)the language that it was asked in and 2) in {Language} if that was not the language the question was asked in."
# # st.write(additional_instructions)

# # Step 1:  Retrieve an Assistant if not already created
# # Initialize OpenAI assistant
# if "assistant" not in st.session_state:
#    openai.api_key = st.secrets["OPENAI_API_KEY"]
#    st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])
#    st.session_state.thread = client.beta.threads.create(
#        metadata={'session_id': st.session_state.session_id}
#    )

# st.markdown("**Ask a question below or select a converation starter**")    

# button_prompt1 = 'How can I be a better Christian example to my team?'
# button_prompt2 = 'How do I better align with my Christian identity'
# button_prompt3 = 'What are 5 scriptures that help me stay positive and resilient'
# button_prompt4 = 'What do I do if I don’t know God’s purpose for my life?'
# button_prompt5 = 'How can I be a servant leader?'
# button_prompt6 = 'What does Ephesians 2:10 mean and how does that apply to me?'

# def disable(disable_button):
#    st.session_state['disabled'] = disable_button
#    st.session_state.input_count += 1

# with st.expander("Conversation Starters"):
#    # Create Predefine prompt buttons
#    if st.button(button_prompt1, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#         st.session_state.prompt = button_prompt1

#    if st.button(button_prompt2, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#         st.session_state.prompt = button_prompt2

#    if st.button(button_prompt3, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#         st.session_state.prompt = button_prompt3

#    if st.button(button_prompt4, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#         st.session_state.prompt = button_prompt4

#    if st.button(button_prompt5, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#         st.session_state.prompt = button_prompt5

#    if st.button(button_prompt6, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#         st.session_state.prompt = button_prompt6


# response_container = st.container()
# spinner_container = st.container()

# typed_input = st.chat_input("What questions or thoughts are on your mind?", on_submit=disable, args=(False,))

# # Check if there is typed input
# if typed_input:
#    st.session_state.prompt = typed_input 

# #Chat input and message creation
# if st.session_state.input_count >= 2:
#    with spinner_container: 
#        with st.spinner("Thinking ...... please give me 30 seconds"):
#            time.sleep(3)
#        with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#            st.write("I'm sorry, I can only support one submission at a time. Could you please re-enter your question?")
#        st.session_state.input_count = 0
# elif st.session_state.prompt and (st.session_state.input_count < 2):
#    with spinner_container:
#        with st.spinner("Thinking ...... please give me 30 seconds"):
#             time.sleep(3)  # Simulate immediate delay
#    if st.session_state.input_count == 1:
#        st.session_state.message = client.beta.threads.messages.create(
#            thread_id=st.session_state.thread.id,
#            role="user",
#            content=st.session_state.prompt
#        )

#        # Step 4: Run the Assistant
#        st.session_state.run = client.beta.threads.runs.create(
#            thread_id=st.session_state.thread.id,
#            assistant_id=st.session_state.assistant.id,
#            additional_instructions=additional_instructions
#        )
#        update_run_status() 
           
#       # Handle run status
#        # Check and handle the run status
#        while st.session_state.run.status != "completed" and st.session_state.retry_error < 3:
#            if st.session_state.run.status == "in_progress":
#                with spinner_container:
#                    with st.spinner("Thinking ...... please give me 30 seconds"):
#                       time.sleep(5)  # Simulate delay
#                update_run_status()  # Update the status after delay
#            else:
#                time.sleep(3)  # Simulate delay
#                with spinner_container:
#                    with st.spinner("Run failed, retrying ......"):
#                        time.sleep(2) # Simulate delay
#                st.session_state.retry_error += 1
#                update_run_status()
#        if st.session_state.retry_error >= 3:
#            with spinner_container:
#                st.error("FAILED: The system is currently processing too many requests. Please try again later ......")
#        else:
#            with response_container:
#                display_results()
    
#        st.session_state.input_count = 0

import openai
import streamlit as st
from openai import OpenAI
from openai import AssistantEventHandler
import uuid

client = OpenAI()

st.set_page_config(page_title="Coach Edge - Virtual Life Coach")

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
   st.session_state.thread = client.beta.threads.create(
       metadata={'session_id': st.session_state.session_id}
   )

#Retrieve URL Parameters
Fname = st.query_params.get("fname", "Unknown")
School = st.query_params.get("school", "Unknown")
Team = st.query_params.get("team", "Unknown")
Role = st.query_params.get("role", "Unknown")
Language=st.query_params.get("language","Unknown")
additional_instructions = f"The users name is {Fname}. They are a {Role} on the {Team} team at the {School}. Provide each response in 2 languages... 1)the language that it was asked in and 2) in {Language} if that was not the language the question was asked in."

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
    st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
    with st.chat_message('user',avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
        st.markdown(st.session_state.prompt)
    with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
        container = st.empty()
        st.session_state.message_thread = client.beta.threads.create(
              messages=[{"role": "user","content": st.session_state.prompt}]
        )
        stream = client.beta.threads.runs.create(
            assistant_id=st.session_state.assistant.id,
            thread_id = st.session_state.message_thread.id,
            additional_instructions = additional_instructions,
            stream = True
        )
        for event in stream:
           if event.data.object == "thread.message.delta":
              for content in event.data.delta.content:
                 if content.type == 'text':
                    delta.append(content.text.value)
                    response = "".join(item for item in delta if item).strip()
                    container.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
