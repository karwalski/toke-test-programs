import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock database of messages for demonstration
    mock_messages = {
        "conv_1": [
            {"id": "msg_1", "content": "Hello there", "sent_at": "2025-12-31T23:00:00Z"},
            {"id": "msg_2", "content": "How are you doing?", "sent_at": "2025-12-31T23:30:00Z"},
            {"id": "msg_3", "content": "Great weather today", "sent_at": "2026-01-01T00:00:00Z"},
            {"id": "msg_4", "content": "See you tomorrow", "sent_at": "2026-01-01T00:00:00Z"},
            {"id": "msg_5", "content": "Let's schedule a meeting", "sent_at": "2026-01-01T00:00:00Z"}
        ],
        "conv_2": [
            {"id": "msg_6", "content": "Different conversation", "sent_at": "2026-01-01T00:00:00Z"}
        ]
    }
    
    # Extract parameters
    conversation_id = input_data.get("conversation_id")
    query = input_data.get("query", "").lower()
    
    # Get messages for the conversation
    conversation_messages = mock_messages.get(conversation_id, [])
    
    # Search for messages containing the query
    matched_messages = []
    for message in conversation_messages:
        if query in message["content"].lower():
            matched_messages.append(message)
    
    # Prepare response
    response = {
        "messages": matched_messages,
        "total": len(matched_messages)
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()