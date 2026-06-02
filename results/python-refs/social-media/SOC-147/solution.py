import json
import sys
import time

def check_service_health():
    start_time = time.time()
    
    # Simulate service health checks
    services = {
        "database": "up",
        "cache": "up",
        "search": "up"
    }
    
    # Calculate response time (simulate 12ms)
    response_time = 12
    
    return {
        "status": "healthy",
        "services": services,
        "response_time_ms": response_time,
        "version": "1.0.0"
    }

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    request = json.loads(input_data)
    
    if request.get("action") == "health_check":
        response = check_service_health()
        print(json.dumps(response, separators=(',', ':')))
    else:
        error_response = {"error": "Invalid action"}
        print(json.dumps(error_response, separators=(',', ':')))

if __name__ == "__main__":
    main()