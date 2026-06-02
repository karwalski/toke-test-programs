import json
import sys
from datetime import datetime, timezone

def parse_iso_time(iso_string):
    return datetime.fromisoformat(iso_string.replace('Z', '+00:00'))

def main():
    # Read input
    current_time_str = input().strip()
    messages_json = input().strip()
    
    current_time = parse_iso_time(current_time_str)
    messages = json.loads(messages_json)
    
    for message in messages:
        text = message["text"]
        ttl_seconds = message["ttl_after_read_seconds"]
        read_at_str = message["read_at"]
        
        if read_at_str is None:
            # Message is unread - timer not started
            print(f"{text}: VISIBLE (timer not started)")
        else:
            # Message has been read
            read_at = parse_iso_time(read_at_str)
            expire_time = read_at.timestamp() + ttl_seconds
            current_timestamp = current_time.timestamp()
            
            if current_timestamp >= expire_time:
                # Message has expired
                seconds_ago = int(current_timestamp - expire_time)
                expire_time_formatted = datetime.fromtimestamp(expire_time, timezone.utc).strftime("%H:%M:%S")
                print(f"{text}: EXPIRED (expired at {expire_time_formatted}, {seconds_ago}s ago)")
            else:
                # Message is still visible
                seconds_remaining = int(expire_time - current_timestamp)
                print(f"{text}: VISIBLE (expires in {seconds_remaining}s)")

if __name__ == "__main__":
    main()