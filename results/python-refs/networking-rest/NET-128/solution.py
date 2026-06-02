import sys
import random
import time

def main():
    # Read input
    url = input().strip()
    start_users = int(input().strip())
    max_users = int(input().strip())
    ramp_duration = int(input().strip())
    
    # Calculate ramp-up step
    user_increment = (max_users - start_users) / ramp_duration
    
    # Simulate stress test for each second
    for second in range(ramp_duration + 1):
        current_users = min(start_users + int(user_increment * second), max_users)
        
        # Simulate realistic metrics based on user load
        base_throughput = 10
        req_per_sec = max(1, int(current_users * base_throughput * random.uniform(0.8, 1.2)))
        
        # Simulate increasing error rate with more users
        error_rate = min(0.1, (current_users - start_users) / (max_users * 10))
        errors = int(req_per_sec * error_rate * random.uniform(0.5, 1.5))
        
        # Simulate p95 latency increasing with load
        base_latency = 50
        load_factor = current_users / max_users
        p95_latency = int(base_latency * (1 + load_factor * 2) * random.uniform(0.9, 1.1))
        
        print(f"users={current_users}, req/s={req_per_sec}, errors={errors}, p95={p95_latency}ms")

if __name__ == "__main__":
    main()