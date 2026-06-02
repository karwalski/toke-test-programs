import json
import sys

def compare_vector_clocks(clock1, clock2):
    """Compare two vector clocks to determine their relationship"""
    all_devices = set(clock1.keys()) | set(clock2.keys())
    
    clock1_greater = False
    clock2_greater = False
    
    for device in all_devices:
        val1 = clock1.get(device, 0)
        val2 = clock2.get(device, 0)
        
        if val1 > val2:
            clock1_greater = True
        elif val2 > val1:
            clock2_greater = True
    
    if clock1_greater and not clock2_greater:
        return "clock1_wins"
    elif clock2_greater and not clock1_greater:
        return "clock2_wins"
    elif clock1_greater and clock2_greater:
        return "concurrent"
    else:
        return "equal"

def format_clock(clock):
    """Format vector clock for output"""
    items = []
    for device in sorted(clock.keys()):
        items.append(f"{device}:{clock[device]}")
    return "{" + ",".join(items) + "}"

def solve():
    # Read input
    devices_line = input().strip()
    events_line = input().strip()
    
    devices = json.loads(devices_line)
    events = json.loads(events_line)
    
    # Group events by message ID
    message_events = {}
    for event in events:
        msg_id = event["msg_id"]
        if msg_id not in message_events:
            message_events[msg_id] = []
        message_events[msg_id].append(event)
    
    # Process each message for conflicts
    conflicts = []
    
    for msg_id, msg_events in message_events.items():
        if len(msg_events) > 1:
            # Check for conflicts between events
            for i in range(len(msg_events)):
                for j in range(i + 1, len(msg_events)):
                    event1 = msg_events[i]
                    event2 = msg_events[j]
                    
                    # Compare vector clocks
                    comparison = compare_vector_clocks(event1["clock"], event2["clock"])
                    
                    # If concurrent and different actions, it's a conflict
                    if comparison == "concurrent" and event1["action"] != event2["action"]:
                        conflicts.append({
                            "msg_id": msg_id,
                            "event1": event1,
                            "event2": event2
                        })
    
    # Output conflicts
    for conflict in conflicts:
        print(f"CONFLICT on {conflict['msg_id']}:")
        print(f"  {conflict['event1']['device']}: {conflict['event1']['action']} {format_clock(conflict['event1']['clock'])}")
        print(f"  {conflict['event2']['device']}: {conflict['event2']['action']} {format_clock(conflict['event2']['clock'])}")
        print("resolution: keep both (concurrent)")

if __name__ == "__main__":
    solve()