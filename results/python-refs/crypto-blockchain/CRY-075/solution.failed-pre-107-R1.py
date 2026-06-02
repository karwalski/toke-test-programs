import hashlib
import json
import sys

def keccak256(data):
    """Simple Keccak-256 implementation using hashlib"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha3_256(data).hexdigest()

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse event signatures from first line
    event_signatures = json.loads(lines[0])
    
    # Process emit commands
    events = []
    
    for i in range(1, len(lines)):
        line = lines[i]
        if line.startswith("EMIT "):
            parts = line[5:].split()  # Remove "EMIT " and split
            event_name = parts[0]
            params = parts[1:] if len(parts) > 1 else []
            
            if event_name in event_signatures:
                # Create signature string
                param_types = event_signatures[event_name]
                signature = f"{event_name}({','.join(param_types)})"
                
                # Calculate keccak256 hash
                topic = keccak256(signature)
                
                # Create event object
                event = {
                    "topic": topic,
                    "data": params
                }
                events.append(event)
    
    # Output as JSON array
    print(json.dumps(events, separators=(',', ':')))

if __name__ == "__main__":
    main()