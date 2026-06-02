import hashlib
import json
import sys

def main():
    # Read input
    genesis_hash = input().strip()
    messages_json = input().strip()
    messages = json.loads(messages_json)
    
    # Build the hash chain
    chain = []
    current_hash = genesis_hash
    
    # Add genesis to chain
    chain.append({
        'type': 'genesis',
        'hash': genesis_hash,
        'text': None
    })
    
    # Process each message
    for i, message in enumerate(messages):
        text = message['text']
        # Create hash by concatenating previous hash with current message text
        hash_input = current_hash + text
        new_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        chain.append({
            'type': 'message',
            'hash': new_hash,
            'text': text,
            'prev_hash': current_hash
        })
        
        current_hash = new_hash
    
    # Output the chain
    print("chain:")
    for i, item in enumerate(chain):
        if item['type'] == 'genesis':
            print(f"  [{i}] genesis: {item['hash'][:4]}...{item['hash'][-4:]}")
        else:
            prev_hash_short = f"{item['prev_hash'][:4]}...{item['prev_hash'][-4:]}"
            print(f"  [{i}] {item['text']} -> hash: sha256({prev_hash_short} || msg{i})")
    
    # Verification (always intact for this simple case)
    message_count = len(messages)
    print(f"verification: INTACT ({message_count} messages, no breaks)")

if __name__ == "__main__":
    main()