# UI helpers for displaying chat
import streamlit as st
from chat_session import get_history

def display_chat(message):
    """
    Displays a chat message. User messages are right-aligned, and bot messages are left-aligned.
    """
    if message['role'] == "user":
        st.markdown(f'<div style="text-align: right; color: #0084ff;">{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left; color: #4e9bff;">{message["text"]}</div>', unsafe_allow_html=True)
    
    # Handle special formatting for code or tables
    if message.get('type') == 'code':
        st.code(message['text'], language='python')
    elif message.get('type') == 'table':
        st.table(message['data'])

def chat_input():
    """
    Displays a text input for the user to type their query.
    """
    return st.text_input("Your message:", "")

def chat_output(text):
    """
    Displays the bot's response.
    """
    st.write(f"Bot: {text}")


# Function to render individual messages (User/System)
def render_message(role, content):
    if role == "user":
        st.markdown(f"**You:** {content}", unsafe_allow_html=True)
    elif role == "system":
        st.markdown(f"**System:** {content}", unsafe_allow_html=True)

# Function to render chat history
def render_chat_history(messages):
    for msg in messages:
        render_message(msg["role"], msg["content"])

def display_chat_html(msg):
    role = msg.get("role", "bot")
    message = msg.get("message", "")
    if role == "user":
        # return f"<div class='user-msg'><b>You:</b> {message}</div>"
        return f"<div class='user-msg' style='background-color: #ffffff; padding: 10px; border-radius: 8px; display: inline-block; max-width: 80%;'><b>You:</b> {message}</div>"

    else:
        return f"<div class='bot-msg'><b>Bot:</b> {message}</div>"

