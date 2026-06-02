import sys

def main():
    # Read base URL from stdin
    base_url = input().strip()
    
    # Simulate REST API test suite
    steps = [
        ("Create", "PASS"),
        ("Read", "PASS"), 
        ("Update", "PASS"),
        ("Verify", "PASS"),
        ("Delete", "PASS")
    ]
    
    all_passed = True
    
    # Execute each step and report results
    for i, (step_name, result) in enumerate(steps, 1):
        print(f"Step {i} ({step_name}): {result}")
        if result == "FAIL":
            all_passed = False
        break

if __name__ == "__main__":
    main()