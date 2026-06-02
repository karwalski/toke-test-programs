import json
import sys

def solve():
    max_depth = int(input().strip())
    events_json = input().strip()
    events = json.loads(events_json)
    
    # Group events by original_msg_id
    chains = {}
    for event in events:
        original_msg_id = event['original_msg_id']
        if original_msg_id not in chains:
            chains[original_msg_id] = []
        chains[original_msg_id].append(event)
    
    # Process each chain
    for original_msg_id in sorted(chains.keys()):
        chain_events = chains[original_msg_id]
        
        # Sort by depth to build the chain correctly
        chain_events.sort(key=lambda x: x['depth'])
        
        # Build the chain path
        path = []
        
        # Start with the first sender
        if chain_events:
            path.append(chain_events[0]['from'])
        
        # Add each recipient in order
        for event in chain_events:
            path.append(event['to'])
        
        # Output the chain
        chain_str = " -> ".join(path)
        print(f"chain {original_msg_id}: {chain_str}")
        
        # Check for max depth violation
        max_event_depth = max(event['depth'] for event in chain_events)
        if max_event_depth >= max_depth:
            print(f"WARNING: max depth reached ({max_event_depth})")
        
        # Check for loops (same person appears twice)
        seen_users = set()
        loop_user = None
        for user in path:
            if user in seen_users:
                loop_user = user
                break
            seen_users.add(user)
        
        if loop_user:
            print(f"WARNING: loop detected ({loop_user} appears twice)")

solve()