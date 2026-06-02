import json
import sys

def analyze_traffic_logs():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    logs = json.loads(input_data)
    
    print("Traffic Summary")
    
    total_requests = 0
    total_errors = 0
    
    # Process each route
    for log in logs:
        from_service = log["from_service"]
        to_service = log["to_service"]
        request_count = log["request_count"]
        error_count = log["error_count"]
        avg_latency_ms = log["avg_latency_ms"]
        
        # Calculate error rate
        error_rate = (error_count / request_count) * 100 if request_count > 0 else 0
        
        # Format error rate to 1 decimal place
        error_rate_str = f"{error_rate:.1f}"
        
        # Print route summary
        print(f"{from_service} -> {to_service}: {request_count} req/s, {error_rate_str}% errors, {avg_latency_ms}ms avg")
        
        # Add to totals
        total_requests += request_count
        total_errors += error_count
    
    # Calculate overall error rate
    overall_error_rate = (total_errors / total_requests) * 100 if total_requests > 0 else 0
    overall_error_rate_str = f"{overall_error_rate:.1f}"
    
    # Print totals
    print(f"Total requests: {total_requests}")
    print(f"Overall error rate: {overall_error_rate_str}%")

if __name__ == "__main__":
    analyze_traffic_logs()