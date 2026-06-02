import json
import sys

def main():
    # Read input
    lines = sys.stdin.read().strip().split('\n')
    
    # Parse first line: rate_per_second burst_size
    rate_per_second, burst_size = map(int, lines[0].split())
    
    # Parse requests JSON
    requests = json.loads(lines[1])
    
    # Token bucket simulation
    tokens = burst_size  # Start with full bucket
    last_time = 0
    
    for request in requests:
        time_ms = request["time_ms"]
        endpoint = request["endpoint"]
        
        # Calculate time elapsed since last request
        time_elapsed_ms = time_ms - last_time
        time_elapsed_s = time_elapsed_ms / 1000.0
        
        # Add tokens based on elapsed time and rate
        tokens_to_add = time_elapsed_s * rate_per_second
        tokens = min(burst_size, tokens + tokens_to_add)
        
        # Check if request can be allowed
        if tokens >= 1:
            tokens -= 1
            status = "ALLOWED"
        else:
            status = "THROTTLED"
        
        print(f"{time_ms} {endpoint}: {status}")
        
        last_time = time_ms

if __name__ == "__main__":
    main()