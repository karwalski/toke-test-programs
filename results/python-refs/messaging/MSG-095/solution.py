import json
import sys

def solve_causal_ordering():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    events = json.loads(input_data)
    
    # Create a mapping from event ID to event data
    event_map = {}
    for event in events:
        event_map[event['event']] = event
    
    # Track processed events and their positions
    processed = set()
    ordered_sequence = []
    violations = []
    
    # Process events in order of their Lamport timestamps
    events_by_timestamp = sorted(events, key=lambda x: (x['lamport_ts'], x['event']))
    
    for event in events_by_timestamp:
        event_id = event['event']
        
        # Check if all dependencies have been processed
        missing_deps = []
        for dep in event['dependencies']:
            if dep not in processed:
                missing_deps.append(dep)
        
        # If there are missing dependencies, check if they should have been processed
        # based on Lamport timestamp ordering
        has_violation = False
        for dep in missing_deps:
            if dep in event_map:
                dep_event = event_map[dep]
                if dep_event['lamport_ts'] < event['lamport_ts']:
                    has_violation = True
                    break
                elif dep_event['lamport_ts'] == event['lamport_ts'] and dep < event_id:
                    has_violation = True
                    break
        
        if has_violation:
            violations.append(f"Event {event_id} has unresolved dependencies: {missing_deps}")
        
        # Add event to ordered sequence
        ordered_sequence.append(f"{event_id}(ts={event['lamport_ts']})")
        processed.add(event_id)
    
    # Generate output
    ordered_str = " -> ".join(ordered_sequence)
    violations_str = "none" if not violations else "; ".join(violations)
    
    print(f"ordered: {ordered_str}")
    print(f"violations: {violations_str}")

if __name__ == "__main__":
    solve_causal_ordering()