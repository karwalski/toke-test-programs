import json
import sys

def rebalance_partitions(consumers, num_partitions):
    if not consumers:
        return {}
    
    consumers.sort()  # Ensure consistent ordering
    assignment = {}
    
    partitions_per_consumer = num_partitions // len(consumers)
    extra_partitions = num_partitions % len(consumers)
    
    partition_idx = 0
    for i, consumer in enumerate(consumers):
        # First 'extra_partitions' consumers get one extra partition
        partitions_to_assign = partitions_per_consumer + (1 if i < extra_partitions else 0)
        assignment[consumer] = list(range(partition_idx, partition_idx + partitions_to_assign))
        partition_idx += partitions_to_assign
    
    return assignment

def format_assignment(assignment):
    result = []
    for consumer in sorted(assignment.keys()):
        partitions_str = ','.join(map(str, assignment[consumer]))
        result.append(f"{consumer}=[{partitions_str}]")
    return ', '.join(result)

# Read input
num_partitions = int(input().strip())
events_json = input().strip()
events = json.loads(events_json)

# Process events
active_consumers = set()

for event in events:
    event_type = event["type"]
    consumer = event["consumer"]
    
    if event_type == "join":
        active_consumers.add(consumer)
        action = "joins"
    elif event_type == "leave":
        active_consumers.discard(consumer)
        action = "leaves"
    
    # Rebalance partitions
    assignment = rebalance_partitions(list(active_consumers), num_partitions)
    
    # Output result
    if assignment:
        assignment_str = format_assignment(assignment)
        print(f"after {consumer} {action}: {assignment_str}")
    else:
        print(f"after {consumer} {action}: ")