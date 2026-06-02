import json
import sys

# Read input from stdin
input_data = json.load(sys.stdin)

running_steps = input_data['running_steps']
now_ms = input_data['now_ms']

timed_out = []
healthy = []

for step in running_steps:
    step_id = step['id']
    started_at_ms = step['started_at_ms']
    timeout_ms = step['timeout_ms']
    
    elapsed_ms = now_ms - started_at_ms
    
    if elapsed_ms > timeout_ms:
        exceeded_by_ms = elapsed_ms - timeout_ms
        timed_out.append({
            "id": step_id,
            "elapsed_ms": elapsed_ms,
            "exceeded_by_ms": exceeded_by_ms
        })
    else:
        healthy.append(step_id)

result = {
    "timed_out": timed_out,
    "healthy": healthy
}

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))