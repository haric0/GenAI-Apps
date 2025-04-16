import streamlit as st

# Dummy credentials for admin
ADMIN_CREDENTIALS = {"username": "admin", "password": "admin123"}

def login():
    """
    Handles the login process and returns the user role.
    Returns 'admin' or 'guest'.
    """
    if "role" in st.session_state:
        return st.session_state["role"]  # Already logged in

    st.sidebar.title("Login")

    # Login form for Admin
    username = st.sidebar.text_input("Username", "")
    password = st.sidebar.text_input("Password", "", type="password")

    if st.sidebar.button("Login"):
        if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
            st.session_state["role"] = "admin"
            st.success("Logged in as Admin")
            return "admin"
        else:
            st.error("Invalid credentials. Please try again.")
            return "guest"
    
    return "guest"  # Default role is guest

def is_admin():
    """
    Checks if the current user is an admin.
    """
    return st.session_state.get("role") == "admin"
