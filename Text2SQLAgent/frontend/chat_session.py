# Handles chat history and session
import streamlit as st
import json
from datetime import datetime

# Initialize the chat history in session state
def init_chat():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

# Add a new message to the chat
def add_message(role, text, msg_type="text", data=None):
    message = {
        "role": role,
        "text": text,
        "type": msg_type,
        "data": data
    }
    st.session_state.chat_history.append(message)

# Get all chat history
# def get_history():
#     return st.session_state.get("chat_history", [])

# In chat_session.py
def get_history():
    """Get the history of messages."""
    # Assuming the history is stored in session state or some list.
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    return st.session_state.chat_history

# Add this debug print to inspect the structure of the history
history = get_history()
print("Chat History:", history)  # This will help you identify the structure



# Clear chat history
def clear_history():
    st.session_state.chat_history = []

# Downloadable history as a JSON file
# def get_downloadable_chat():
#     chat_data = json.dumps(st.session_state.get("chat_history", []), indent=2)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"chat_history_{timestamp}.json"
#     st.download_button("Download Chat History", chat_data, file_name=filename, mime="application/json")

# In chat_session.py

def get_downloadable_chat():
    """Returns chat history in a downloadable string format."""
    history = get_history()  # Retrieve chat history (assumed to be a list of messages)
    if not history:
        return ""
    
    # Concatenate chat history into a string format
    chat_text = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "Bot"
        
        # Check for available keys in the message dictionary
        message_content = msg.get("message") or msg.get("text") or msg.get("content", "No message content")
        chat_text += f"{role}: {message_content}\n"
    
    return chat_text
