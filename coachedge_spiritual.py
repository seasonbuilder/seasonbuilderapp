# import openai
# import time
# import datetime
# import uuid
# import streamlit as st
# from openai import OpenAI
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# st.set_page_config(page_title="Coach Edge - Virtual Life Coach")
 
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;} 
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)

# st.markdown("""
#     <style>
#            .block-container {
#                 padding-top: 1rem;
#                 padding-left: 1rem;
#                 padding-right: 1rem;
#             }
#     </style>
#     """, unsafe_allow_html=True)

# # Function to update the run status (simulating the retrieval process)
# def update_run_status():
#     # Retrieving run status
#     st.session_state.run = client.beta.threads.runs.retrieve(
#         thread_id=st.session_state.thread.id,
#         run_id=st.session_state.run.id,
#     )
   
# def display_results():
#     # Find the next empty Google shet row
#     next_row = find_next_empty_row(sheet)
#     # Write data to the next row
#     sheet.update(f"A{next_row}:B{next_row}", [[formatted_datetime, st.session_state.prompt]])
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
                 
# # Function to find next empty Google Sheets row
# def find_next_empty_row(sheet):
#     all_values = sheet.get_all_values()
#     return len(all_values) + 1

# #Use creds to create a client to interact with the Google Drive API
# scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
#          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# google_service_account_info = st.secrets['google_service_account']
# creds = ServiceAccountCredentials.from_json_keyfile_dict(google_service_account_info, scope)
# gclient = gspread.authorize(creds)

# # Initialize the client
# client = OpenAI()
# sheet = gclient.open(st.secrets["spreadsheet"]).sheet1
    




# # Initialize session state variables

# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# if "run" not in st.session_state:
#     st.session_state.run = {"status": None}

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "retry_error" not in st.session_state:
#     st.session_state.retry_error = 0

# if 'prompt' not in st.session_state:
#     st.session_state.prompt = ''

# if 'input_count' not in st.session_state:
#     st.session_state.input_count = 0

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


# #Retrieve URL Parameters
# st.session_state.fname = st.query_params.get("fname", "Unknown")
# st.session_state.school = st.query_params.get("school", "Unknown")
# st.session_state.team = st.query_params.get("team", "Unknown")
# st.session_state.role = st.query_params.get("role", "Unknown")
# st.session_state.language=st.query_params.get("language","Unknown")

# additional_instructions = f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} on the {st.session_state.team} team at the {st.session_state.school} and their native language is {st.session_state.language}. If the response is not given to them in their native language, give a response in their native language too."
# #st.write(additional_instructions)

# # Step 1:  Retrieve an Assistant if not already created
# # Initialize OpenAI assistant
# if "assistant" not in st.session_state:
#     openai.api_key = st.secrets["OPENAI_API_KEY"]
#     st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])
#     st.session_state.thread = client.beta.threads.create(
#         metadata={'session_id': st.session_state.session_id}
#     )

# # Get the current date and time
# current_datetime = datetime.datetime.now()
# formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")  # Format as desired

# st.markdown("**Ask a question below or select a converation starter**")    

# button_prompt1 = 'How can I be a better Christian example to my team?'
# button_prompt2 = 'How do I better align with my Christian identity'
# button_prompt3 = 'What are 5 scriptures that help me stay positive and resilient'
# button_prompt4 = 'What do I do if I don’t know God’s purpose for my life?'
# button_prompt5 = 'How can I be a servant leader?'
# button_prompt6 = 'What does Ephesians 2:10 mean and how does that apply to me?'

# def disable(disable_button):
#     st.session_state['disabled'] = disable_button
#     st.session_state.input_count += 1

# with st.expander("Conversation Starters"):
#     # Create Predefine prompt buttons
#     if st.button(button_prompt1, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#          st.session_state.prompt = button_prompt1

#     if st.button(button_prompt2, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#          st.session_state.prompt = button_prompt2

#     if st.button(button_prompt3, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#          st.session_state.prompt = button_prompt3

#     if st.button(button_prompt4, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#          st.session_state.prompt = button_prompt4

#     if st.button(button_prompt5, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#          st.session_state.prompt = button_prompt5

#     if st.button(button_prompt6, on_click=disable, args=(False,), disabled=st.session_state.get("disabled", False)):
#          st.session_state.prompt = button_prompt6


# response_container = st.container()
# spinner_container = st.container()

# typed_input = st.chat_input("What's on your mind?", on_submit=disable, args=(False,))

# # Check if there is typed input
# if typed_input:
#     st.session_state.prompt = typed_input 

# #Chat input and message creation
# if st.session_state.input_count >= 2:
#     with spinner_container: 
#         with st.spinner("Thinking ...... please give me 30 seconds"):
#             time.sleep(3)
#         with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#             st.write("I'm sorry, I can only support one submission at a time. Could you please re-enter your question?")
#         st.session_state.input_count = 0
# elif st.session_state.prompt and (st.session_state.input_count < 2):
#     with spinner_container:
#         with st.spinner("Thinking ...... please give me 30 seconds"):
#              time.sleep(3)  # Simulate immediate delay
#     if st.session_state.input_count == 1:
#         st.session_state.message = client.beta.threads.messages.create(
#             thread_id=st.session_state.thread.id,
#             role="user",
#             content=st.session_state.prompt
#         )

#         # Step 4: Run the Assistant
#         st.session_state.run = client.beta.threads.runs.create(
#             thread_id=st.session_state.thread.id,
#             assistant_id=st.session_state.assistant.id,
#             additional_instructions=additional_instructions
#         )
#         update_run_status() 
            
#         # Handle run status
#         # Check and handle the run status
#         while st.session_state.run.status != "completed" and st.session_state.retry_error < 3:
#             if st.session_state.run.status == "in_progress":
#                 with spinner_container:
#                     with st.spinner("Thinking ...... please give me 30 seconds"):
#                        time.sleep(5)  # Simulate delay
#                 update_run_status()  # Update the status after delay
#             else:
#                  time.sleep(3)  # Simulate delay
#                  with spinner_container:
#                     with st.spinner("Run failed, retrying ......"):
#                         time.sleep(2) # Simulate delay
#                  st.session_state.retry_error += 1
#                  update_run_status()
#         if st.session_state.retry_error >= 3:
#             with spinner_container:
#                 st.error("FAILED: The system is currently processing too many requests. Please try again later ......")
#         else:
#             with response_container:
#                 display_results()
     
#     st.session_state.input_count = 0

import openai
import streamlit as st
from openai import OpenAI
import uuid

client = OpenAI()

st.set_page_config(page_title="Coach Edge - Virtual Life Coach")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;} 
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

#st.markdown("""
 #   <style>
  #         .block-container {
   #             padding-top: 0rem;
    #            padding-left: 0rem;
     #           padding-right: 0rem;
      #      }
    #</style>
    #""", unsafe_allow_html=True)

# Initialize session state variables

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

additional_instructions = f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} on the {st.session_state.team} team at the {st.session_state.school} and their native language is {st.session_state.language}. If the response is not given to them in their native language, give a response in their native language too."

st.markdown("**Ask a question below or select a conversation starter from the list below**")    

button_prompt1 = 'How can I be a better Christian example to my team?'
button_prompt2 = 'How do I better align with my Christian identity'
button_prompt3 = 'What are 5 scriptures that help me stay positive and resilient'
button_prompt4 = 'What do I do if I don’t know God’s purpose for my life?'
button_prompt5 = 'How can I be a servant leader?'
button_prompt6 = 'What does Ephesians 2:10 mean and how does that apply to me?'

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
        for event in stream:
           if event.data.object == "thread.message.delta":
              for content in event.data.delta.content:
                 if content.type == 'text':
                    delta.append(content.text.value)
                    response = "".join(item for item in delta if item).strip()
                    container.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
