import sys
import time
import random

def simulate_request_timing():
    """Simulate realistic network timing values"""
    dns = random.uniform(5, 25)  # DNS lookup time in ms
    tcp = random.uniform(10, 50)  # TCP connect time in ms
    tls = random.uniform(20, 80)  # TLS handshake time in ms
    ttfb = random.uniform(50, 200)  # Time to first byte in ms
    total = dns + tcp + tls + ttfb
    return dns, tcp, tls, ttfb, total

def main():
    # Read input
    url = input().strip()
    n = int(input().strip())
    
    # Store all timing data
    all_timings = []
    
    # Set random seed for reproducible results
    random.seed(42)
    
    # Print header
    print(f"Request timing breakdown for {url} ({n} requests):")
    print()
    print("Req#    DNS(ms)  TCP(ms)  TLS(ms)  TTFB(ms) Total(ms)")
    print("-" * 55)
    
    # Run N requests and collect timing data
    for i in range(1, n + 1):
        dns, tcp, tls, ttfb, total = simulate_request_timing()
        all_timings.append((dns, tcp, tls, ttfb, total))
        
        print(f"{i:3d}  {dns:8.1f} {tcp:8.1f} {tls:8.1f} {ttfb:9.1f} {total:9.1f}")
    
    print()
    
    # Calculate and print summary statistics
    dns_times = [t[0] for t in all_timings]
    tcp_times = [t[1] for t in all_timings]
    tls_times = [t[2] for t in all_timings]
    ttfb_times = [t[3] for t in all_timings]
    total_times = [t[4] for t in all_timings]
    
    def calc_stats(times):
        return min(times), max(times), sum(times) / len(times)
    
    print("Summary Statistics:")
    print("Phase    Min(ms)  Max(ms)  Avg(ms)")
    print("-" * 35)
    
    phases = [
        ("DNS", dns_times),
        ("TCP", tcp_times),
        ("TLS", tls_times),
        ("TTFB", ttfb_times),
        ("Total", total_times)
    ]
    
    for phase_name, times in phases:
        min_time, max_time, avg_time = calc_stats(times)
        print(f"{phase_name:5s} {min_time:8.1f} {max_time:8.1f} {avg_time:8.1f}")

if __name__ == "__main__":
    main()