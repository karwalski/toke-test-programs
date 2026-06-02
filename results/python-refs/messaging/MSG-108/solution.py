import json
import sys

# Read input
heartbeat_timeout = int(input().strip())
heartbeat_events_json = input().strip()
check_time = int(input().strip())

# Parse heartbeat events
heartbeat_events = json.loads(heartbeat_events_json)

# Track last heartbeat time for each consumer
last_heartbeat = {}

# Process all heartbeat events
for event in heartbeat_events:
    consumer = event["consumer"]
    time_ms = event["time"]
    last_heartbeat[consumer] = time_ms

# Check each consumer's status at check_time
dead_consumers = []
consumers = sorted(last_heartbeat.keys())

for consumer in consumers:
    last_time = last_heartbeat[consumer]
    time_since_last = check_time - last_time
    
    if time_since_last > heartbeat_timeout:
        print(f"{consumer}: DEAD (last heartbeat {time_since_last}ms ago at t={last_time})")
        dead_consumers.append(consumer)
    else:
        print(f"{consumer}: alive")

# Trigger rebalance if any consumers are dead
if dead_consumers:
    print(f"ACTION: rebalance triggered ({len(dead_consumers)} dead consumers)")