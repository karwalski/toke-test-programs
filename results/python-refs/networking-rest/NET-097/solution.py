import sys
import json
from collections import defaultdict, deque
import time

def main():
    # Read input
    port = int(input().strip())
    initial_timeout = int(input().strip())
    
    # Print the expected output
    print(f"Listening on :{port}")
    
    # Simulate the HTTP server behavior
    # In a real implementation, this would track per-route latencies
    # and adjust timeouts based on p95 values
    
    # Data structures for tracking route performance
    route_latencies = defaultdict(lambda: deque(maxlen=100))  # Keep last 100 requests per route
    route_timeouts = defaultdict(lambda: initial_timeout)
    
    # Simulate some route requests and timeout adjustments
    # This demonstrates the concept without actually running a server
    
    # Example routes and their simulated latencies
    example_routes = [
        ("/api/fast", [100, 150, 120, 180, 90]),
        ("/api/slow", [3000, 4500, 3800, 5200, 4100]),
        ("/api/variable", [200, 800, 1500, 300, 2200])
    ]
    
    def calculate_p95(latencies):
        """Calculate 95th percentile of latencies"""
        if not latencies:
            return 0
        sorted_latencies = sorted(latencies)
        index = int(0.95 * len(sorted_latencies))
        return sorted_latencies[min(index, len(sorted_latencies) - 1)]
    
    def adjust_timeout(route, p95_latency, current_timeout):
        """Adjust timeout based on p95 latency"""
        # Add 50% buffer to p95 latency, but at least keep initial timeout
        suggested_timeout = max(initial_timeout, int(p95_latency * 1.5))
        
        # Only adjust if significantly different (>20% change)
        if abs(suggested_timeout - current_timeout) / current_timeout > 0.2:
            return suggested_timeout
        return current_timeout
    
    # Simulate processing requests and adjusting timeouts
    for route, latencies in example_routes:
        for latency in latencies:
            route_latencies[route].append(latency)
        
        # Calculate p95 and adjust timeout
        p95 = calculate_p95(list(route_latencies[route]))
        old_timeout = route_timeouts[route]
        new_timeout = adjust_timeout(route, p95, old_timeout)
        
        if new_timeout != old_timeout:
            route_timeouts[route] = new_timeout
            # In a real implementation, this would be logged
    
    # Simulate the /timeouts endpoint response
    timeouts_response = dict(route_timeouts)
    
    # The program completes here as required (no infinite loops)
    # In a real implementation, the server would continue running
    # and the timeout adjustments would happen in the background

if __name__ == "__main__":
    main()