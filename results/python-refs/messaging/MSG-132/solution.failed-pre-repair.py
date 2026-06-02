import json
import sys
from datetime import datetime

def parse_time(time_str):
    """Parse time string in HH:MM:SS.mmm format and return milliseconds since midnight"""
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds_parts = parts[2].split('.')
    seconds = int(seconds_parts[0])
    milliseconds = int(seconds_parts[1])
    
    total_ms = hours * 3600000 + minutes * 60000 + seconds * 1000 + milliseconds
    return total_ms

def calculate_percentile(data, percentile):
    """Calculate the given percentile of the data"""
    if not data:
        return 0
    
    data_sorted = sorted(data)
    n = len(data_sorted)
    
    if percentile == 50:
        if n % 2 == 0:
            return (data_sorted[n//2 - 1] + data_sorted[n//2]) / 2
        else:
            return data_sorted[n//2]
    elif percentile == 95:
        index = int(0.95 * (n - 1))
        return data_sorted[index]
    elif percentile == 99:
        index = int(0.99 * (n - 1))
        return data_sorted[index]

def main():
    # Read input
    sla_line = input().strip()
    events_line = input().strip()
    
    # Parse JSON
    sla = json.loads(sla_line)
    events = json.loads(events_line)
    
    # Calculate latencies
    latencies = []
    for event in events:
        sent_ms = parse_time(event['sent_at'])
        delivered_ms = parse_time(event['delivered_at'])
        latency = delivered_ms - sent_ms
        latencies.append(latency)
    
    # Output latencies
    latency_strs = [f"{lat}ms" for lat in latencies]
    print(f"latencies: [{', '.join(latency_strs)}]")
    
    # Calculate percentiles
    p50 = calculate_percentile(latencies, 50)
    p95 = calculate_percentile(latencies, 95)
    p99 = calculate_percentile(latencies, 99)
    
    # Check SLA compliance
    targets_met = 0
    total_targets = 3
    
    # p50 check
    p50_status = "OK" if p50 <= sla['p50_ms'] else "BREACH"
    if p50_status == "OK":
        targets_met += 1
    print(f"p50: {int(p50)}ms (target: {sla['p50_ms']}ms) {p50_status}")
    
    # p95 check
    p95_status = "OK" if p95 <= sla['p95_ms'] else "BREACH"
    if p95_status == "OK":
        targets_met += 1
    print(f"p95: {int(p95)}ms (target: {sla['p95_ms']}ms) {p95_status}")
    
    # p99 check
    p99_status = "OK" if p99 <= sla['p99_ms'] else "BREACH"
    if p99_status == "OK":
        targets_met += 1
    print(f"p99: {int(p99)}ms (target: {sla['p99_ms']}ms) {p99_status}")
    
    # Calculate compliance percentage
    compliance_pct = (targets_met / total_targets) * 100
    print(f"SLA compliance: {targets_met}/{total_targets} targets met ({compliance_pct:.1f}%)")

if __name__ == "__main__":
    main()