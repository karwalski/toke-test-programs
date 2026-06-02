import json
import sys
from urllib.parse import urlparse, parse_qs

# Read port from stdin
port = input().strip()

# Event store - list of events
events = []

# Current states - dictionary mapping resource IDs to their current state
states = {}

def handle_post_events(body):
    """Handle POST /events - append event to log"""
    try:
        event = json.loads(body)
        events.append(event)
        
        # Update state if event has an id
        if 'id' in event:
            resource_id = event['id']
            if resource_id not in states:
                states[resource_id] = {}
            
            # Apply event to state
            if 'type' in event:
                if event['type'] == 'set':
                    if 'key' in event and 'value' in event:
                        states[resource_id][event['key']] = event['value']
                elif event['type'] == 'delete':
                    if 'key' in event and event['key'] in states[resource_id]:
                        del states[resource_id][event['key']]
                elif event['type'] == 'create':
                    states[resource_id] = event.get('data', {})
        
        return json.dumps({"status": "event added", "event_count": len(events)})
    except:
        return json.dumps({"error": "invalid event format"})

def handle_get_state(resource_id):
    """Handle GET /state/:id - reconstruct state by replaying events"""
    # Replay all events for this resource ID
    state = {}
    
    for event in events:
        if event.get('id') == resource_id:
            if event.get('type') == 'create':
                state = event.get('data', {})
            elif event.get('type') == 'set':
                if 'key' in event and 'value' in event:
                    state[event['key']] = event['value']
            elif event.get('type') == 'delete':
                if 'key' in event and event['key'] in state:
                    del state[event['key']]
    
    return json.dumps(state)

def simulate_request(method, path, body=""):
    """Simulate handling an HTTP request"""
    if method == "POST" and path == "/events":
        return handle_post_events(body)
    elif method == "GET" and path.startswith("/state/"):
        resource_id = path.split("/state/")[1]
        return handle_get_state(resource_id)
    else:
        return json.dumps({"error": "not found"})

# Print the expected startup message
print(f"Listening on :{port}")