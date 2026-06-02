import urllib.request
import time
import sys

def main():
    # Read input
    n = int(input().strip())
    url = input().strip()
    
    latencies = []
    
    # Make N requests and measure latency
    for i in range(n):
        start_time = time.time()
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                response.read()
        except:
            pass  # Continue even if request fails
        end_time = time.time()
        
        latency_ms = int((end_time - start_time) * 1000)
        latencies.append(latency_ms)
        print(f"req {i + 1}: {latency_ms}ms")
    
    # Calculate statistics
    min_latency = min(latencies)
    max_latency = max(latencies)
    mean_latency = int(sum(latencies) / len(latencies))
    
    # Calculate p95 (95th percentile)
    sorted_latencies = sorted(latencies)
    p95_index = int(0.95 * len(sorted_latencies))
    if p95_index >= len(sorted_latencies):
        p95_index = len(sorted_latencies) - 1
    p95_latency = sorted_latencies[p95_index]
    
    print(f"min: {min_latency}ms | max: {max_latency}ms | mean: {mean_latency}ms | p95: {p95_latency}ms")

if __name__ == "__main__":
    main()