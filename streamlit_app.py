import requests

# python 3.8 (3.8.16) or it doesn't work
# pip install streamlit streamlit-chat langchain python-dotenv
import streamlit as st
from streamlit_chat import message

API_URL = "https://wilkie-hf-space-tuto.hf.space/api/v1/prediction/44ea4a5d-ba88-4f29-813c-47f71225c429"


def query(payload):
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errhtp:
        st.write("HTTP Error: ", errhtp)
        return None
    except requests.exceptions.ConnectionError as errcon:
        st.write("Connection Error: ", errcon)
        return None
    except requests.exceptions.Timeout as errtime:
        st.write("Timeout Error: ", errtime)
        return None
    except requests.exceptions.RequestException as err:
        st.write("Something went wrong. Please try again.", err)
        return None
    
    try:
        return response.json()
    except Exception as exc:
        st.write("Parsing Response Error: ", exc)
        return None
 output = query({
    "question": "Hey, how are you?",
    "overrideConfig": {
        "sessionId": "example",
        "memoryKey": "example",
        "serpApiKey": "example",
        "systemMessage": "example",
    }
})   
    
# Initialize the conversation history if not available in session_state
if "conversation" not in st.session_state:
        st.session_state.conversation = []
            
# setup streamlit page
st.set_page_config(page_title="Smart Doc AI", page_icon=":books:")
st.header("🤖 Smart Doc AI")

# User input
user_input = st.text_input("Enter your question here: ") #, key="user_input")
submit_button = st.button("Submit")

if submit_button:
        # Add user input to conversation history
        st.session_state['conversation'].append({'role': 'user', 'content': user_input})
        with st.spinner("Generating answer..."):
        # Query the API
            response = query(({'history': st.session_state['conversation'], 'question': user_input}))
            if response is not None:
                # Add chatbot response to conversation history
                st.session_state['conversation'].append({'role': 'bot', 'content': response})
            else:
                st.session_state['conversation'].append({'role': 'bot', 'content': 'Sorry, I am unable to process your request at the moment.'})
            
# Display converstion history
conversation = st.session_state.get('conversation', [])
for i, msg in enumerate(conversation[:]):
    if i % 2 == 0:
        message(msg['content'], is_user=True, key=str(i) + '_user')
    else:
        message(msg['content'], is_user=False, key=str(i) + '_ai')
    
