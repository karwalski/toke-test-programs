import json
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    events = json.loads(input_data)
    
    # Group events by message ID
    messages = {}
    
    for event in events:
        msg_id = event['msg_id']
        if msg_id not in messages:
            messages[msg_id] = {
                'state': 'ACTIVE',
                'uploaded': None,
                'views': [],
                'screenshots': [],
                'expired': None,
                'deleted': None
            }
        
        msg = messages[msg_id]
        event_type = event['event']
        time = event['time']
        user = event['user']
        
        if event_type == 'upload':
            msg['uploaded'] = (time, user)
            msg['state'] = 'ACTIVE'
        elif event_type == 'view':
            msg['views'].append((time, user))
        elif event_type == 'screenshot':
            msg['screenshots'].append((time, user))
        elif event_type == 'expire':
            msg['expired'] = time
            msg['state'] = 'EXPIRED'
        elif event_type == 'delete':
            msg['deleted'] = time
            msg['state'] = 'DELETED'
    
    # Generate output for each message
    for msg_id in sorted(messages.keys()):
        msg = messages[msg_id]
        
        print(f"{msg_id}:")
        print(f"  state: {msg['state']}")
        
        if msg['uploaded']:
            time, user = msg['uploaded']
            print(f"  uploaded: {time} by {user}")
        
        view_count = len(msg['views'])
        if view_count == 0:
            print("  views: 0")
        elif view_count == 1:
            time, user = msg['views'][0]
            print(f"  views: 1 ({user} at {time})")
        else:
            view_list = ", ".join(f"{user} at {time}" for time, user in msg['views'])
            print(f"  views: {view_count} ({view_list})")
        
        for time, user in msg['screenshots']:
            print(f"  ALERT: screenshot by {user} at {time}")
        
        if msg['expired']:
            print(f"  expired: {msg['expired']}")
        
        if msg['deleted']:
            print(f"  deleted: {msg['deleted']}")

if __name__ == "__main__":
    main()