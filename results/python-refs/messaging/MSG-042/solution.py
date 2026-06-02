import json
import sys
from datetime import datetime

def format_iso_time(iso_string):
    # Parse ISO format and return formatted string
    dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse metadata (first line)
    metadata = json.loads(lines[0])
    room_name = metadata["room"]
    exported_at = format_iso_time(metadata["exported_at"])
    
    # Parse messages (remaining lines)
    messages = []
    for line in lines[1:]:
        if line:  # Skip empty lines
            message = json.loads(line)
            messages.append(message)
    
    # Output formatted chat export
    print(f"Chat Export: {room_name}")
    print(f"Exported: {exported_at} UTC")
    print("=" * 32)
    
    for message in messages:
        sender = message["sender"]
        time = format_iso_time(message["time"])
        text = message["text"]
        print(f"[{time}] {sender}: {text}")
    
    print("=" * 32)
    print(f"{len(messages)} messages exported")

if __name__ == "__main__":
    main()