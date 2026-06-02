import json
import sys

def analyze_traffic_logs():
    input_data = sys.stdin.read().strip()
    logs = json.loads(input_data)
    
    print("Traffic Summary")
    
    total_requests = 0
    total_errors = 0
    
    logs.sort(key=lambda x: x["request_count"], reverse=True)
    
    for log in logs:
        from_service = log["from_service"]
        to_service = log["to_service"]
        request_count = log["request_count"]
        error_count = log["error_count"]
        avg_latency_ms = log["avg_latency_ms"]
        
        error_rate = (error_count / request_count) * 100 if request_count > 0 else 0
        # Round half up to 1 decimal
        error_rate_rounded = int(error_rate * 10 + 0.5) / 10
        error_rate_str = f"{error_rate_rounded:.1f}"
        
        print(f"{from_service} -> {to_service}: {request_count} req/s, {error_rate_str}% errors, {avg_latency_ms}ms avg")
        
        total_requests += request_count
        total_errors += error_count
    
    overall_error_rate = (total_errors / total_requests) * 100 if total_requests > 0 else 0
    overall_rounded = int(overall_error_rate * 10 + 0.5) / 10
    overall_error_rate_str = f"{overall_rounded:.1f}"
    
    print(f"Total requests: {total_requests}")
    print(f"Overall error rate: {overall_error_rate_str}%")

if __name__ == "__main__":
    analyze_traffic_logs()