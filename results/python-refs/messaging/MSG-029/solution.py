import json
from datetime import datetime, timedelta

def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M:%S")

def main():
    threshold = int(input().strip())
    messages_json = input().strip()
    messages = json.loads(messages_json)
    
    # Convert times and sort by timestamp
    for msg in messages:
        msg['parsed_time'] = parse_time(msg['time'])
    messages.sort(key=lambda x: x['parsed_time'])
    
    flagged = {}
    
    # Check each message as a potential end of a 60-second window
    for i, msg in enumerate(messages):
        sender = msg['sender']
        end_time = msg['parsed_time']
        start_time = end_time - timedelta(seconds=60)
        
        # Count messages from this sender in the 60-second window ending at this message
        count = 0
        for j in range(len(messages)):
            other_msg = messages[j]
            if (other_msg['sender'] == sender and 
                start_time < other_msg['parsed_time'] <= end_time):
                count += 1
        
        # If count exceeds threshold, flag this sender
        if count > threshold:
            if sender not in flagged or count > flagged[sender]:
                flagged[sender] = count
    
    # Output flagged senders
    for sender, count in flagged.items():
        print(f"FLAGGED: {sender} ({count} messages in 60s, threshold: {threshold})")

if __name__ == "__main__":
    main()