import json
import sys

def generate_hook(data):
    subject = data["subject"]
    topic = data["topic"]
    grade_level = data["grade_level"]
    hook_type = data["hook_type"]
    
    # Generate different types of hooks based on hook_type
    if hook_type == "question":
        if subject == "Science" and topic == "Gravity":
            hook_content = "If there were no gravity, what would happen to everything on Earth?"
        else:
            hook_content = f"What do you think you know about {topic}?"
    elif hook_type == "story":
        hook_content = f"Imagine a world where {topic} works differently than it does today..."
    elif hook_type == "fact":
        hook_content = f"Did you know that {topic} affects our daily lives in surprising ways?"
    else:
        hook_content = f"Let's explore the fascinating world of {topic}!"
    
    # Format the output
    header = f"Lesson Hook: {topic} ({subject}, Grade {grade_level})"
    
    if hook_type == "question":
        hook_line = f"Opening Question: {hook_content}"
    elif hook_type == "story":
        hook_line = f"Opening Story: {hook_content}"
    elif hook_type == "fact":
        hook_line = f"Opening Fact: {hook_content}"
    else:
        hook_line = f"Opening Hook: {hook_content}"
    
    purpose = f"Purpose: Activate prior knowledge and curiosity about {topic}."
    
    return f"{header}\n{hook_line}\n{purpose}"

# Read input from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

# Generate and print the hook
result = generate_hook(data)
print(result)