# Python Training Script
# Start with basic concepts for DevOps automation

# 1. Hello World - Basic output
print("Hello, DevOps World!")

# 2. Variables and data types
name = "Austin"
age = 25  # Update with your age
print(f"My name is {name} and I'm {age} years old.")

# 3. Lists - Useful for handling multiple items like files or servers
tools = ["Git", "Docker", "Python", "AWS"]
print("DevOps tools I'm learning:", tools)

# 4. Simple function - Reusable code blocks
def greet_user(username):
    return f"Welcome to DevOps learning, {username}!"

print(greet_user("Austin"))

# 5. File operations - Essential for automation scripts
import os

def list_files(directory="."):
    """List all files in a directory"""
    try:
        files = os.listdir(directory)
        print(f"Files in {directory}:")
        for file in files:
            print(f"  - {file}")
    except Exception as e:
        print(f"Error: {e}")

list_files()
