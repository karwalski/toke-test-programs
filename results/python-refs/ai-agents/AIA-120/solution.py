import json
import sys
import math

def calculate_delay(backoff_type, initial_delay_ms, attempt_count):
    if backoff_type == "exponential":
        return initial_delay_ms * (2 ** (attempt_count - 1))
    elif backoff_type == "linear":
        return initial_delay_ms * attempt_count
    elif backoff_type == "fixed":
        return initial_delay_ms
    else:
        return initial_delay_ms

def should_retry_step(data):
    step = data["step"]
    error = data["error"]
    policy = data["policy"]
    
    step_id = step["id"]
    attempt_count = step["attempt_count"]
    error_type = error["type"]
    is_transient = error.get("transient", False)
    max_retries = policy["max_retries"]
    backoff_type = policy["backoff_type"]
    initial_delay_ms = policy["initial_delay_ms"]
    
    # Check if we should retry
    should_retry = False
    delay_ms = None
    reason = ""
    
    if attempt_count >= max_retries:
        should_retry = False
        delay_ms = None
        reason = f"Max retries ({max_retries}) exceeded"
    elif not is_transient:
        should_retry = False
        delay_ms = None
        reason = "Non-transient error"
    else:
        should_retry = True
        delay_ms = calculate_delay(backoff_type, initial_delay_ms, attempt_count)
        reason = f"Transient error, attempt {attempt_count} of {max_retries}, {backoff_type} backoff"
    
    return {
        "should_retry": should_retry,
        "delay_ms": delay_ms,
        "reason": reason
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Process the data
result = should_retry_step(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))