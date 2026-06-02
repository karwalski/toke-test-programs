import json
import sys

def build_thread_tree(messages):
    # Create a dictionary to store messages by ID for quick lookup
    message_dict = {msg['id']: msg for msg in messages}
    
    # Create a dictionary to store children for each message
    children = {}
    roots = []
    
    # Build the tree structure
    for msg in messages:
        if msg['reply_to'] is None:
            roots.append(msg)
        else:
            parent_id = msg['reply_to']
            if parent_id not in children:
                children[parent_id] = []
            children[parent_id].append(msg)
    
    return roots, children

def print_thread(message, children, level=0):
    # Print current message with proper indentation
    indent = "  " * level
    print(f"{indent}{message['sender']}: {message['text']}")
    
    # Print all children recursively
    if message['id'] in children:
        for child in children[message['id']]:
            print_thread(child, children, level + 1)

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    messages = json.loads(input_data)
    
    # Build the tree structure
    roots, children = build_thread_tree(messages)
    
    # Print the thread view
    for root in roots:
        print_thread(root, children)

if __name__ == "__main__":
    main()