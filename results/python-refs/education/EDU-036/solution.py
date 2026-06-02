import json
import sys

def print_mind_map(data, prefix="", is_last=True, is_root=True):
    if is_root:
        print(data["topic"])
        subtopics = data.get("subtopics", [])
    else:
        connector = "└── " if is_last else "├── "
        if isinstance(data, str):
            print(prefix + connector + data)
            return
        else:
            print(prefix + connector + data["name"])
            subtopics = data.get("subtopics", [])
    
    for i, subtopic in enumerate(subtopics):
        is_last_subtopic = (i == len(subtopics) - 1)
        
        if is_root:
            new_prefix = ""
        else:
            new_prefix = prefix + ("    " if is_last else "│   ")
        
        print_mind_map(subtopic, new_prefix, is_last_subtopic, False)

# Read JSON from stdin
input_data = json.loads(sys.stdin.read().strip())
print_mind_map(input_data)