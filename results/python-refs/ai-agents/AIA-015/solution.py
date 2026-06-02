import json
import sys

def calculate_next_retry():
    # Read input from stdin
    input_data = json.load(sys.stdin)
    
    attempts = input_data['attempts']
    base_delay_ms = input_data['base_delay_ms']
    max_delay_ms = input_data['max_delay_ms']
    max_retries = input_data['max_retries']
    
    # Count failed attempts
    failed_attempts = [attempt for attempt in attempts if not attempt['success']]
    attempt_number = len(failed_attempts) + 1
    
    # Check if we should retry
    should_retry = len(failed_attempts) < max_retries
    
    if not should_retry:
        result = {
            "should_retry": False,
            "next_attempt_ms": None,
            "attempt_number": attempt_number
        }
    else:
        # Calculate exponential backoff delay
        # For attempt n, delay = base_delay * 2^(n-1)
        delay = base_delay_ms * (2 ** (len(failed_attempts)))
        delay = min(delay, max_delay_ms)
        
        # Get timestamp of last failed attempt
        last_attempt_time = failed_attempts[-1]['timestamp_ms']
        next_attempt_ms = last_attempt_time + delay
        
        result = {
            "should_retry": True,
            "next_attempt_ms": next_attempt_ms,
            "attempt_number": attempt_number
        }
    
    # Output JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    calculate_next_retry()