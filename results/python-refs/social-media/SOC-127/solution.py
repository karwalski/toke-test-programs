import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract parameters
    action = input_data.get("action")
    token = input_data.get("token")
    conversation_id = input_data.get("conversation_id")
    cursor = input_data.get("cursor")
    limit = input_data.get("limit")
    
    # Mock message data (in a real implementation, this would come from a database)
    all_messages = {
        "conv_1": [
            {
                "id": "msg_1",
                "sender": "alice",
                "content": "Hey!",
                "sent_at": "2026-01-01T00:00:00Z",
                "read": True
            }
        ]
    }
    
    # Get messages for the conversation
    messages = all_messages.get(conversation_id, [])
    
    # Apply pagination (simplified - in real implementation would use cursor properly)
    if cursor is None:
        # Start from beginning
        start_index = 0
    else:
        # In real implementation, cursor would be decoded to find position
        start_index = 0
    
    # Get the page of messages
    page_messages = messages[start_index:start_index + limit]
    
    # Determine next cursor (simplified - would be more complex in real implementation)
    next_cursor = None
    if start_index + limit < len(messages):
        next_cursor = f"cursor_{start_index + limit}"
    
    # Create response
    response = {
        "conversation_id": conversation_id,
        "messages": page_messages,
        "next_cursor": next_cursor
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()