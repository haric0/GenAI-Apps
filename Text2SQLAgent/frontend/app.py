import streamlit as st
import requests
from chat_session import init_chat, get_history, add_message, clear_history, get_downloadable_chat
from ui_utils import display_chat

# Dummy login credentials
VALID_USERS = {"admin": "admin123"}

# Dummy backend API endpoints
BACKEND_CHAT_API = "http://localhost:8000/api/chat"
BACKEND_SCHEMA_API = "http://localhost:8000/api/update_schema"

# BACKEND_CHAT_API = "http://host.docker.internal:8000/api/chat"
# BACKEND_SCHEMA_API = "http://host.docker.internal:8000/api/update_schema"


st.set_page_config(page_title="Text2SQL Chat", layout="wide")
st.title("🧠 Text2SQL Chat Assistant")

# Initialize chat session
init_chat()

# --- LOGIN SCREEN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = "guest"

if not st.session_state.logged_in:
    st.sidebar.subheader("🔐 Login")
    role_option = st.sidebar.radio("Select User Role", ["Guest", "Admin"])

    if role_option == "Admin":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.user_role = "admin"
            else:
                st.sidebar.error("Invalid credentials.")
    else:
        if st.sidebar.button("Continue as Guest"):
            st.session_state.logged_in = True
            st.session_state.user_role = "guest"

# --- MAIN UI AFTER LOGIN ---
if st.session_state.logged_in:
    role = st.session_state.user_role
    st.sidebar.success(f"Logged in as {role.capitalize()}")
    if st.sidebar.button("❌ Logout"):
        st.session_state.logged_in = False
        clear_history()
        st.experimental_rerun()

    # Admin-specific tools
    if role == "admin":
        st.subheader("📦 Update DB Schema")
        uploaded_file = st.file_uploader("Upload your schema file (JSON/SQL/etc.)")
        if st.button("Upload Schema") and uploaded_file:
            response = requests.post(BACKEND_SCHEMA_API, files={"file": uploaded_file})
            if response.status_code == 200:
                st.success("Schema updated successfully!")
            else:
                st.error("Failed to update schema.")

    # Guest and Admin both see chat
    st.subheader("💬 Ask Your Question")
    
    # --- Display the chat history ---
    with st.container():
        for msg in get_history():
            display_chat(msg)

    # --- Submit Button and Input Box ---    
    # Adding an empty container to place the input box at the bottom
    input_container = st.container()

    with input_container:
        user_input = st.text_input("Type your query here...")

        # Submit button for sending the message
        submit_btn = st.button("Submit")

        # Handle user input and call the API
        if submit_btn and user_input:
            # Add user message to chat history before calling API
            add_message("user", user_input)

            try:
                # Call the backend API
                response = requests.post(BACKEND_CHAT_API, json={"query": user_input})
                
                if response.status_code == 200:
                    bot_reply = response.json().get("response", "No response.")
                    add_message("bot", bot_reply)
                else:
                    add_message("bot", "❌ Error reaching the backend.")
            except Exception as e:
                add_message("bot", f"⚠️ Exception: {str(e)}")

    # --- Download chat history ---
    st.download_button("📥 Download Chat History", get_downloadable_chat(), file_name="chat_history.txt")

