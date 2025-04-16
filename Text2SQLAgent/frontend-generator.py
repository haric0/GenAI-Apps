import os

# Define structure and placeholder content
project_structure = {
    "frontend": {
        "app.py": "# Main Streamlit app\n",
        "auth.py": "# Handles login and user roles\n",
        "config.py": "# Dummy credentials\n",
        "ui_utils.py": "# UI helpers for displaying chat\n",
        "chat_session.py": "# Handles chat history and session\n",
        "Dockerfile": "# Dockerfile to run Streamlit app\n",
        "static": {
            "styles.css": "/* Custom styles */\n"
        }
    }
}

# Recursive function to create folders and files
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):  # it's a folder
            create_structure(path, content)
        else:
            with open(path, "w") as f:
                f.write(content)

# Create the project
create_structure(".", project_structure)

print("✅ Frontend folder structure created.")
