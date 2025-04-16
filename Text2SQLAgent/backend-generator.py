import os

# Folder and file structure definition
structure = {
    "backend/api": ["chat.py", "schema.py"],
    "backend/core": ["config.py", "db.py", "faiss_handler.py", "logger.py", "prompter.py"],
    "backend/data": [],  # For storing uploaded schemas
    "backend/logs": ["app.log"],
    "backend/models": ["request_models.py", "response_models.py"],
    "backend/scripts": ["start_server.sh"],
    "backend/faiss_service": ["faiss_main.py", "Dockerfile", "requirements.txt"],
    "backend": ["main.py", "Dockerfile", "requirements.txt"],
    "backend/utils": ["schema_parser.py", "faiss_utils.py", "utils.py"],

}

def create_structure():
    for folder, files in structure.items():
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Created folder: {folder}")
        for file in files:
            file_path = os.path.join(folder, file)
            with open(file_path, "w") as f:
                if file.endswith(".py"):
                    f.write(f"# {file}\n")
            print(f"  └─ 📝 Created file: {file_path}")
    print("\n✅ Backend project structure initialized successfully!")

if __name__ == "__main__":
    create_structure()

