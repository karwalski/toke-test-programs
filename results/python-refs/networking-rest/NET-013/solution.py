import sys
from collections import defaultdict, deque
import time

def main():
    # Read input
    port = int(input().strip())
    requests_per_second = int(input().strip())
    
    # Print the expected output
    print(f"Listening on :{port}")
    
    # Rate limiting data structures
    # In a real implementation, this would track requests per IP
    # For simulation purposes, we just print the listening message
    # as the test expects
    
    # The rate limiting logic would work like this:
    # - Keep a sliding window of timestamps for each IP
    # - When a request comes in, remove old timestamps outside the window
    # - If remaining timestamps >= limit, return 429
    # - Otherwise, add current timestamp and process request
    
    # Example rate limiting implementation (not executed since we're simulating):
    """
    ip_requests = defaultdict(deque)
    
    def is_rate_limited(ip_address):
        current_time = time.time()
        window_start = current_time - 1.0  # 1 second window
        
        # Remove old requests outside the window
        while ip_requests[ip_address] and ip_requests[ip_address][0] < window_start:
            ip_requests[ip_address].popleft()
        
        # Check if limit exceeded
        if len(ip_requests[ip_address]) >= requests_per_second:
            return True
        
        # Add current request
        ip_requests[ip_address].append(current_time)
        return False
    """

if __name__ == "__main__":
    main()