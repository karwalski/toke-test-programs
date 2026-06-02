import json
import sys

def simulate_heartbeat():
    # Read input
    interval = int(input().strip())
    threshold = int(input().strip())
    events_json = input().strip()
    events = json.loads(events_json)
    
    # Create a set of times when pongs were received
    pong_times = set()
    for event in events:
        if event["type"] == "pong":
            pong_times.add(event["time"])
    
    # Find the maximum time to simulate
    max_time = 0
    if events:
        max_time = max(event["time"] for event in events)
    
    # Simulate heartbeat protocol
    current_time = 0
    missed_count = 0
    
    while current_time <= max_time:
        # Check if we received a pong at this time
        if current_time in pong_times:
            missed_count = 0
            print(f"{current_time}ms: ALIVE")
        else:
            missed_count += 1
            if missed_count >= threshold:
                print(f"{current_time}ms: TIMEOUT")
            else:
                print(f"{current_time}ms: ALIVE")
        
        current_time += interval

if __name__ == "__main__":
    simulate_heartbeat()