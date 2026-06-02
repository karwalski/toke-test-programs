import json
import sys
from datetime import datetime

def main():
    lines = sys.stdin.read().strip().split('\n')
    target_user = lines[0]
    messages = json.loads(lines[1])
    metadata = json.loads(lines[2])
    
    timestamp = "[timestamp]"
    
    sent_messages = [msg for msg in messages if msg['sender'] == target_user]
    received_messages = [msg for msg in messages if msg['recipient'] == target_user]
    
    sent_messages.sort(key=lambda m: m['time'])
    received_messages.sort(key=lambda m: m['time'])
    
    print(f"GDPR DATA EXPORT: {target_user}")
    print(f"generated: {timestamp}")
    print("---")
    
    print("PROFILE:")
    if 'profile' in metadata:
        for key, value in metadata['profile'].items():
            print(f"  {key}: {value}")
    
    for key, value in metadata.items():
        if key != 'profile':
            print(f"  {key}: {value}")
    
    print(f"MESSAGES SENT ({len(sent_messages)}):")
    if sent_messages:
        for msg in sent_messages:
            print(f"  [{msg['time']}] to {msg['recipient']}: {msg['text']}")
    else:
        print("  (none)")
    
    print(f"MESSAGES RECEIVED ({len(received_messages)}):")
    if received_messages:
        for msg in received_messages:
            print(f"  [{msg['time']}] from {msg['sender']}: {msg['text']}")
    else:
        print("  (none)")
    
    categories = ["profile", "messages", "metadata"]
    print(f"DATA CATEGORIES: {', '.join(categories)}")

if __name__ == "__main__":
    main()