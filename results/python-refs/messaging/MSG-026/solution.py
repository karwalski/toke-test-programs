import json

# Read input
bucket_capacity = int(input().strip())
refill_rate = int(input().strip())
events_json = input().strip()
events = json.loads(events_json)

# Initialize token bucket
tokens = bucket_capacity
last_refill_time = 0

for event in events:
    current_time = event["time"]
    
    # Calculate tokens to add based on time elapsed
    time_elapsed = (current_time - last_refill_time) / 1000.0  # convert ms to seconds
    tokens_to_add = time_elapsed * refill_rate
    tokens = min(bucket_capacity, tokens + tokens_to_add)
    last_refill_time = current_time
    
    # Check if message can be sent
    if tokens >= 1:
        tokens -= 1
        print(f"{current_time}ms: ALLOWED ({int(tokens)} tokens)")
    else:
        print(f"{current_time}ms: REJECTED ({int(tokens)} tokens)")