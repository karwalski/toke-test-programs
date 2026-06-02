import json
import sys
from collections import defaultdict

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    reactions = json.loads(input_data)
    
    # Dictionary to store message reactions
    # Structure: {msg_id: {emoji: set(users)}}
    message_reactions = defaultdict(lambda: defaultdict(set))
    
    # Process each reaction event
    for reaction in reactions:
        msg_id = reaction["msg_id"]
        user = reaction["user"]
        emoji = reaction["emoji"]
        action = reaction["action"]
        
        if action == "add":
            message_reactions[msg_id][emoji].add(user)
        elif action == "remove":
            message_reactions[msg_id][emoji].discard(user)
    
    # Sort messages by ID for consistent output
    sorted_messages = sorted(message_reactions.keys())
    
    # Output the results
    for msg_id in sorted_messages:
        print(f"{msg_id}:")
        
        # Get emojis and sort them for consistent output
        emojis = message_reactions[msg_id]
        # Filter out emojis with no users (after removals)
        active_emojis = {emoji: users for emoji, users in emojis.items() if users}
        
        # Sort emojis by name for consistent output
        sorted_emojis = sorted(active_emojis.keys())
        
        for emoji in sorted_emojis:
            users = active_emojis[emoji]
            count = len(users)
            user_list = ", ".join(sorted(users))  # Sort users for consistent output
            print(f"  {emoji} ({count}): {user_list}")

if __name__ == "__main__":
    main()