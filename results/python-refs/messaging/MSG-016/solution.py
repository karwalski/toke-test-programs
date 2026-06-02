import json
import sys
from datetime import datetime

def format_timestamp(timestamp_str):
    dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    return dt.strftime('%H:%M')

def main():
    current_user = input().strip()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        message = json.loads(line)
        sender = message['sender']
        timestamp = message['timestamp']
        text = message['text']
        
        formatted_time = format_timestamp(timestamp)
        
        if sender == current_user:
            print(f"> [{formatted_time}] {sender}: {text}")
        else:
            print(f"< [{formatted_time}] {sender}: {text}")

if __name__ == "__main__":
    main()