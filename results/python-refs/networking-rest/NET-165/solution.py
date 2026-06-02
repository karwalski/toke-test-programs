import sys
import random
import statistics

def simulate_latency_measurements(n):
    """Simulate n latency measurements in milliseconds"""
    random.seed(42)  # For consistent results
    latencies = []
    
    for _ in range(n):
        # Simulate realistic web request latencies (50-500ms with some outliers)
        base_latency = random.normalvariate(150, 50)
        # Ensure positive values and add occasional spikes
        if random.random() < 0.05:  # 5% chance of spike
            base_latency += random.uniform(200, 800)
        latency = max(10, base_latency)  # Minimum 10ms
        latencies.append(latency)
    
    return latencies

def calculate_percentile(data, percentile):
    """Calculate percentile from sorted data"""
    if not data:
        return 0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (percentile / 100)
    f = int(k)
    c = k - f
    if f == len(sorted_data) - 1:
        return sorted_data[f]
    return sorted_data[f] * (1 - c) + sorted_data[f + 1] * c

def main():
    # Read number of requests
    n = int(input().strip())
    
    # Read URLs
    urls = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            urls.append(line)
        except EOFError:
            break
    
    # Process each URL
    for url in urls:
        # Simulate latency measurements
        latencies = simulate_latency_measurements(n)
        
        # Calculate statistics
        mean_latency = statistics.mean(latencies)
        stddev_latency = statistics.stdev(latencies) if len(latencies) > 1 else 0
        min_latency = min(latencies)
        max_latency = max(latencies)
        p50 = calculate_percentile(latencies, 50)
        p95 = calculate_percentile(latencies, 95)
        p99 = calculate_percentile(latencies, 99)
        
        # Print results
        print(f"URL: {url}")
        print(f"N: {n}")
        print(f"mean: {mean_latency:.2f}ms")
        print(f"stddev: {stddev_latency:.2f}ms")
        print(f"min: {min_latency:.2f}ms")
        print(f"p50: {p50:.2f}ms")
        print(f"p95: {p95:.2f}ms")
        print(f"p99: {p99:.2f}ms")
        print(f"max: {max_latency:.2f}ms")
        print()

if __name__ == "__main__":
    main()