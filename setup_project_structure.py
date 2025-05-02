import os

# Define folder structure
folders = [
    "mpin_security_checker",
    "mpin_security_checker/data",
    "mpin_security_checker/models",
    "mpin_security_checker/utils"
]

files = {
    "mpin_security_checker/main.py": "",
    "mpin_security_checker/utils/pattern_checker.py": "",
    "mpin_security_checker/utils/model_utils.py": "",
    "mpin_security_checker/requirements.txt": ""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create base files
for file_path, content in files.items():
    with open(file_path, 'w') as f:
        f.write(content)

print("✅ MPIN project structure created successfully!")
