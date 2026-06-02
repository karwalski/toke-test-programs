import json

# Read input
max_retries = int(input().strip())
initial_backoff = int(input().strip())
backoff_multiplier = float(input().strip())
outcomes = json.loads(input().strip())

# Initialize variables
current_time = 0
backoff = initial_backoff
attempt = 1

# Process attempts
for i, success in enumerate(outcomes):
    if i >= max_retries:
        break
    
    if success:
        print(f"attempt {attempt} at {current_time}ms: SUCCESS")
        break
    else:
        print(f"attempt {attempt} at {current_time}ms: FAILED")
        if i < len(outcomes) - 1 and attempt < max_retries:
            current_time += backoff
            backoff = int(backoff * backoff_multiplier)
        attempt += 1
else:
    # If we didn't break out of the loop (no success), check if we should print FAILED
    if not any(outcomes[:max_retries]):
        print(f"FAILED after {min(len(outcomes), max_retries)} attempts")