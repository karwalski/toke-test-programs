import json
import sys
import re
from datetime import datetime

def validate_uuid(uuid_string):
    """Validate UUID format"""
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(uuid_pattern, uuid_string, re.IGNORECASE))

def validate_iso_timestamp(timestamp_string):
    """Validate ISO 8601 timestamp format"""
    try:
        datetime.fromisoformat(timestamp_string.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

def validate_message_envelope(json_string):
    """Validate JSON message envelope and return validation result"""
    errors = []
    
    # Try to parse JSON
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError:
        return False, ["Invalid JSON format"]
    
    # Check if data is a dictionary
    if not isinstance(data, dict):
        return False, ["Message envelope must be a JSON object"]
    
    # Required fields
    required_fields = ['id', 'timestamp', 'sender', 'recipient', 'type', 'payload']
    
    # Check for missing fields
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # If missing fields, return early
    if errors:
        return False, errors
    
    # Validate field formats
    if not validate_uuid(data['id']):
        errors.append("Invalid UUID format for 'id' field")
    
    if not validate_iso_timestamp(data['timestamp']):
        errors.append("Invalid ISO 8601 timestamp format for 'timestamp' field")
    
    # Check that sender, recipient, type, and payload are strings
    for field in ['sender', 'recipient', 'type', 'payload']:
        if not isinstance(data[field], str):
            errors.append(f"Field '{field}' must be a string")
    
    # Check for empty strings
    for field in ['sender', 'recipient', 'type']:
        if isinstance(data[field], str) and not data[field].strip():
            errors.append(f"Field '{field}' cannot be empty")
    
    if errors:
        return False, errors
    
    return True, data

def main():
    # Read input from stdin
    json_string = sys.stdin.read().strip()
    
    # Validate the message envelope
    is_valid, result = validate_message_envelope(json_string)
    
    if is_valid:
        print("VALID")
        print(f"sender={result['sender']}")
        print(f"recipient={result['recipient']}")
        print(f"type={result['type']}")
        print(f"payload={result['payload']}")
    else:
        print("INVALID")
        for error in result:
            print(error)

if __name__ == "__main__":
    main()