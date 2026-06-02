import json
import sys

def generate_health_dashboard():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    services = json.loads(input_data)
    
    # Print dashboard header
    print("Service Health Dashboard")
    print()
    
    # Track UP services
    up_count = 0
    total_count = len(services)
    
    # Process each service
    for service in services:
        status = service["status"]
        name = service["service"]
        latency = service["latency_ms"]
        uptime = service["uptime_pct"]
        
        # Count UP services
        if status == "UP":
            up_count += 1
        
        # Format and print service line
        print(f"[{status}] {name:<6} {latency}ms   {uptime}% uptime")
    
    # Print summary
    print()
    print(f"All UP: {up_count}/{total_count}")

if __name__ == "__main__":
    generate_health_dashboard()