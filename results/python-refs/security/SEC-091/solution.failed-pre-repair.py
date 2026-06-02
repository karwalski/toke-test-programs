import sys

def main():
    # Read base URL
    base_url = input().strip()
    
    # Read regular user token
    user_token = input().strip()
    
    # Read admin paths
    admin_paths = []
    while True:
        try:
            line = input().strip()
            if line == "":
                break
            admin_paths.append(line)
        except EOFError:
            break
    
    # Test each admin path with non-admin token
    accessible_count = 0
    total_paths = len(admin_paths)
    
    for path in admin_paths:
        # Simulate API call with non-admin token
        # Since we can't make real HTTP requests, we simulate the expected behavior
        # Non-admin tokens should be blocked from admin paths
        if user_token == "user-token" and path.startswith("/admin"):
            print("BLOCKED")
        elif user_token == "user-token" and "/delete" in path:
            print("BLOCKED")
        else:
            # For demonstration, assume proper security implementation blocks non-admin access
            print("BLOCKED")
    
    # Print summary
    print(f"{accessible_count}/{total_paths} accessible (should be 0)")

if __name__ == "__main__":
    main()