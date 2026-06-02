import json
import sys
from datetime import datetime

def parse_iso_time(iso_string):
    return datetime.fromisoformat(iso_string.replace('Z', '+00:00'))

def main():
    input_data = sys.stdin.read().strip()
    events = json.loads(input_data)
    
    # Group events by message ID
    messages = {}
    
    for event in events:
        msg_id = event['msg_id']
        event_type = event['event']
        timestamp = parse_iso_time(event['time'])
        
        if msg_id not in messages:
            messages[msg_id] = {}
        
        messages[msg_id][event_type] = timestamp
    
    # Process each message
    for msg_id, events_dict in messages.items():
        current_state = 'sent'
        if 'read' in events_dict:
            current_state = 'read'
        elif 'delivered' in events_dict:
            current_state = 'delivered'
        
        # Calculate time differences
        time_parts = []
        total_time = 0
        
        if 'sent' in events_dict and 'delivered' in events_dict:
            sent_to_delivered = int((events_dict['delivered'] - events_dict['sent']).total_seconds())
            time_parts.append(f"sent->delivered: {sent_to_delivered}s")
            total_time += sent_to_delivered
        
        if 'delivered' in events_dict and 'read' in events_dict:
            delivered_to_read = int((events_dict['read'] - events_dict['delivered']).total_seconds())
            time_parts.append(f"delivered->read: {delivered_to_read}s")
            total_time += delivered_to_read
        
        # Format output
        if time_parts:
            time_str = ", ".join(time_parts) + f", total: {total_time}s"
            print(f"{msg_id}: {current_state} ({time_str})")
        else:
            print(f"{msg_id}: {current_state}")

if __name__ == "__main__":
    main()