import json
import sys
from datetime import datetime

def main():
    # Read input
    lines = sys.stdin.read().strip().split('\n')
    target_user = lines[0]
    messages = json.loads(lines[1])
    metadata = json.loads(lines[2])
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    # Filter messages for the target user
    sent_messages = [msg for msg in messages if msg['sender'] == target_user]
    received_messages = [msg for msg in messages if msg['recipient'] == target_user]
    
    # Start output
    print(f"GDPR DATA EXPORT: {target_user}")
    print(f"generated: {timestamp}")
    print("---")
    
    # Profile section
    print("PROFILE:")
    if 'profile' in metadata:
        for key, value in metadata['profile'].items():
            print(f"  {key}: {value}")
    
    # Add other top-level metadata fields to profile
    for key, value in metadata.items():
        if key != 'profile':
            print(f"  {key}: {value}")
    
    # Messages sent section
    print(f"MESSAGES SENT ({len(sent_messages)}):")
    for msg in sent_messages:
        print(f"  [{msg['time']}] to {msg['recipient']}: {msg['text']}")
    
    # Messages received section
    print(f"MESSAGES RECEIVED ({len(received_messages)}):")
    for msg in received_messages:
        print(f"  [{msg['time']}] from {msg['sender']}: {msg['text']}")
    
    # Data categories
    categories = []
    if 'profile' in metadata or any(key != 'profile' for key in metadata.keys()):
        categories.append("profile")
    if sent_messages or received_messages:
        categories.append("messages")
    if metadata:
        categories.append("metadata")
    
    print(f"DATA CATEGORIES: {', '.join(categories)}")

if __name__ == "__main__":
    main()