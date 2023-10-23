import streamlit as st
import streamlit.components.v1 as components
import openai
import pickle
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import faiss
from langchain.vectorstores import FAISS
import os
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from streamlit import session_state as state
import prompts
from pathlib import Path
import psycopg2
from PIL import Image

###connection details from Azure where the pickle files are stored and updated.
connection_string = os.getenv('AZURE_CONNECTION_STRING')
container_name = os.getenv('AZURE_CONTAINER_NAME')

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def load_from_blob(blob_name):
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    serialized_data = blob_client.download_blob().readall()
    data = pickle.loads(serialized_data)
    return data

def save_to_blob(data, blob_name):
    serialized_data = pickle.dumps(data)
    blob_client = blob_service_client.get_blob_client(container_name,blob_name)
    blob_client.upload_blob(serialized_data, overwrite=True)

# Initialize the page count
if 'page_count' not in st.session_state:
    try:
        page_count = load_from_blob('viewcount.pkl')
        st.session_state.page_count = page_count
        st.session_state.page_count += 1 #increment
    except Exception as e:
        st.session_state.page_count = 0

# Display the page count
st.write("Page Visits:", st.session_state.page_count)


# Save the updated page count to the blob storage
save_to_blob(st.session_state.page_count, 'viewcount.pkl')


###page formatting

st.markdown("<h7 style='text-align: center; color: green;'>Please read below terms of use carefully:</h7>", unsafe_allow_html=True)

with open('resources.txt','r') as f:
    file_content = f.read()
st.write(file_content)

st.write('Examples:')
image1 = Image.open(str(Path.cwd())+"//miscellaneous//example.jpg")
st.image(image1, width=800)

'----'

image2 = Image.open(str(Path.cwd())+"//miscellaneous//example2.png")
st.image(image2,width=800)

'----'

#initialize session state (buttonaccept) for accept button
if 'buttonaccept' not in st.session_state:
    st.session_state['buttonaccept'] = False


#dotenv_path = str(Path)+'\\.env'  # Replace with the actual file path
#load_dotenv(dotenv_path)



#initialize buttonaccept for st.session_state
if 'buttonaccept' not in st.session_state:
    st.session_state['buttonaccept'] = False



# ElephantSQL PostgreSQL database connection
DATABASE_URL = os.getenv("DATABASE_URL")

def create_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def inserttodb(prompt,full_response,feedback):
    conn = create_connection()
    cursor = conn.cursor()
    insert_query = "INSERT INTO feedback_chatapp (prompt, full_response, feedback) VALUES (%s, %s, %s)"
    cursor.execute(insert_query,(prompt,full_response, feedback))
    conn.commit()
    cursor.close()
    conn.close() 


#The code consists of two main functions: run_app and clicked.

#The run_app function handles the main logic of the application.
#It displays a title, shows previous chat messages, prompts the user for 
#input, and retrieves the assistant's response. 
#If the response is not "yes," it displays the response and provides feedback buttons. 
#The previous prompt and full response are stored in the st.session_state to be accessed later.

#The clicked function is called when a feedback button is clicked. 
#It determines the feedback type based on the button clicked (1 for positive, 2 for negative) and 
#inserts the previous prompt, full response, and feedback type into the database using the inserttodb 
#function. The st.session_state is then updated to clear the clicked button.

def clicked(button):
    if button == 1:
        feedback = 'Positive'
    elif button == 2:
        feedback = 'Negative'
    else:
        feedback = 'Neutral'
    
    inserttodb(st.session_state.prev_prompt, st.session_state.prev_full_response, feedback)
    st.session_state.clicked = None

def run_app(state):
    st.markdown("<h3 style='text-align: center; color: Green;'>Student Financial Aid Information - Virtual Assistant 🚀</h3>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "prev_prompt" not in st.session_state:
        st.session_state.prev_prompt = None

    if "prev_full_response" not in st.session_state:
        st.session_state.prev_full_response = None


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help you?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        answer = prompts.get_answer(f"{prompt}") # Inference prompt via Hugging Face
        full_response = answer # Display answer

        if full_response != "yes":
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown(full_response)
                
            #add before buttons as buttons within buttons resets session_states. 
                st.session_state.prev_prompt = prompt
                st.session_state.prev_full_response = full_response
                col1,col2 = st.columns(2)
                with col1:
                    st.button('👍', on_click=clicked, args=[1])
                with col2:
                    st.button('👎', on_click=clicked, args=[2])

    return state




#check if user clicks on Accept, once clicked run_app(),
#the else statement outside the nested if block preserves state for run_app()

if not st.session_state.buttonaccept:
    if st.button('Accept'):
        st.session_state.buttonaccept = True
        st.session_state.buttonaccept = run_app(st.session_state.buttonaccept)
else:
    
    st.session_state.buttonaccept= run_app(st.session_state.buttonaccept)
