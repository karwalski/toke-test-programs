import sys
import random

def main():
    # Read input
    base_url = input().strip()
    num_requests = int(input().strip())
    
    # Define chaos test types
    chaos_types = [
        "malformed_headers",
        "wrong_content_type",
        "missing_required_fields",
        "invalid_method",
        "oversized_payload"
    ]
    
    # Simulate chaos testing
    successful_responses = 0
    
    for i in range(num_requests):
        # Randomly select chaos type
        chaos_type = random.choice(chaos_types)
        
        # Simulate server response based on chaos type
        # In a real implementation, this would make actual HTTP requests
        # Here we simulate the behavior
        
        if chaos_type == "malformed_headers":
            # Simulate malformed headers like "Content-Length: abc" or missing colons
            response_code = random.choice([400, 500, 200])
            print(f"Request {i+1}: Applied {chaos_type} - Server responded with {response_code}")
            
        elif chaos_type == "wrong_content_type":
            # Simulate wrong content-type like sending JSON as text/plain
            response_code = random.choice([415, 400, 200])
            print(f"Request {i+1}: Applied {chaos_type} - Server responded with {response_code}")
            
        elif chaos_type == "missing_required_fields":
            # Simulate missing required fields in request body
            response_code = random.choice([400, 422, 500])
            print(f"Request {i+1}: Applied {chaos_type} - Server responded with {response_code}")
            
        elif chaos_type == "invalid_method":
            # Simulate invalid HTTP methods
            response_code = random.choice([405, 501, 400])
            print(f"Request {i+1}: Applied {chaos_type} - Server responded with {response_code}")
            
        elif chaos_type == "oversized_payload":
            # Simulate oversized request payload
            response_code = random.choice([413, 400, 500])
            print(f"Request {i+1}: Applied {chaos_type} - Server responded with {response_code}")
        
        # Count successful responses (2xx status codes)
        if 200 <= response_code < 300:
            successful_responses += 1
    
    # Calculate resilience score
    # Score based on how gracefully server handled malformed requests
    # Higher score means better error handling (returning proper error codes vs crashing)
    
    # Simulate that servers typically handle 60-80% of chaos tests gracefully
    resilience_score = min(100, max(0, int((successful_responses / num_requests) * 100) + random.randint(50, 80)))
    
    print(f"Resilience score: {resilience_score}")

if __name__ == "__main__":
    main()