import sys
import random

def simulate_ping(host, count):
    # Set seed based on host for consistent results
    random.seed(hash(host) % 1000)
    
    # Simulate ping times (in milliseconds)
    ping_times = []
    lost_packets = 0
    
    for _ in range(count):
        # Simulate packet loss (small probability)
        if random.random() < 0.05:  # 5% chance of packet loss
            lost_packets += 1
        else:
            # Generate realistic ping time (0.1ms to 100ms)
            ping_time = random.uniform(0.1, 100.0)
            ping_times.append(ping_time)
    
    # Calculate statistics
    if ping_times:
        min_time = min(ping_times)
        max_time = max(ping_times)
        avg_time = sum(ping_times) / len(ping_times)
    else:
        min_time = max_time = avg_time = 0
    
    loss_percentage = (lost_packets / count) * 100
    
    return min_time, avg_time, max_time, loss_percentage

def main():
    lines = sys.stdin.read().strip().split('\n')
    count = int(lines[0])
    hosts = lines[1:]
    
    for host in hosts:
        if host.strip():
            min_time, avg_time, max_time, loss_pct = simulate_ping(host.strip(), count)
            print(f"{host.strip()}: min={min_time:.0f}ms avg={avg_time:.0f}ms max={max_time:.0f}ms loss={loss_pct:.0f}%")

if __name__ == "__main__":
    main()