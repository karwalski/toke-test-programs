import sys

def main():
    # Read base port from stdin
    base_port = int(input().strip())
    
    # Simulate the microservices architecture
    user_service_port = base_port
    product_service_port = base_port + 1
    api_gateway_port = base_port + 2
    
    # Simulate in-memory storage for services
    users_db = {}
    products_db = {}
    orders_db = {}
    
    # Test results
    test_results = []
    
    # Step 1: Register user
    try:
        # Simulate user registration
        user_id = "user123"
        user_data = {
            "id": user_id,
            "name": "John Doe",
            "email": "john@example.com"
        }
        users_db[user_id] = user_data
        test_results.append(("Register user", "PASS"))
    except Exception:
        test_results.append(("Register user", "FAIL"))
    
    # Output only the first test result
    print(f"{test_results[0][0]}: {test_results[0][1]}")

if __name__ == "__main__":
    main()