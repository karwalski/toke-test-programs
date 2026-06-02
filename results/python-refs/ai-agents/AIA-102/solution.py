import json
import sys
from datetime import datetime

def format_and_validate_message():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    raw_message = input_data["raw_message"]
    protocol = input_data["protocol"]
    
    # Initialize formatted message
    formatted_message = {}
    valid = True
    
    # Map raw message fields to protocol fields
    field_mapping = {
        "from": "sender",
        "to": "receiver",
        "msg": "payload",
        "message": "payload",
        "data": "payload"
    }
    
    # Process each required field
    required_fields = protocol["required_fields"]
    valid_types = protocol.get("types", [])
    
    for field in required_fields:
        if field == "sender":
            if "from" in raw_message:
                formatted_message["sender"] = raw_message["from"]
            elif "sender" in raw_message:
                formatted_message["sender"] = raw_message["sender"]
            else:
                formatted_message["sender"] = None
                valid = False
                
        elif field == "receiver":
            if "to" in raw_message:
                formatted_message["receiver"] = raw_message["to"]
            elif "receiver" in raw_message:
                formatted_message["receiver"] = raw_message["receiver"]
            else:
                formatted_message["receiver"] = None
                valid = False
                
        elif field == "type":
            if "type" in raw_message:
                msg_type = raw_message["type"]
            else:
                # Try to infer type from message content
                msg_content = raw_message.get("msg", "").lower()
                if "done" in msg_content or "completed" in msg_content:
                    msg_type = "notification"
                elif "?" in msg_content or "request" in msg_content:
                    msg_type = "request"
                else:
                    msg_type = "notification"
            
            formatted_message["type"] = msg_type
            if valid_types and msg_type not in valid_types:
                valid = False
                
        elif field == "payload":
            if "msg" in raw_message:
                formatted_message["payload"] = raw_message["msg"]
            elif "payload" in raw_message:
                formatted_message["payload"] = raw_message["payload"]
            elif "message" in raw_message:
                formatted_message["payload"] = raw_message["message"]
            elif "data" in raw_message:
                formatted_message["payload"] = raw_message["data"]
            else:
                formatted_message["payload"] = None
                valid = False
                
        elif field == "timestamp":
            if "timestamp" in raw_message:
                formatted_message["timestamp"] = raw_message["timestamp"]
            else:
                formatted_message["timestamp"] = None
                valid = False
        else:
            # For any other required field not present
            formatted_message[field] = raw_message.get(field, None)
            if field not in raw_message:
                valid = False
    
    # Check if any required field is None
    for field in required_fields:
        if formatted_message.get(field) is None:
            valid = False
    
    # Output result
    result = {
        "formatted_message": formatted_message,
        "valid": valid
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    format_and_validate_message()