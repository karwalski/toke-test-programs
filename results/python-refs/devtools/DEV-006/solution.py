import json
import subprocess
import sys

def run_test_manifest():
    # Read JSON manifest from stdin
    input_data = sys.stdin.read()
    manifest = json.loads(input_data)
    
    command = manifest["command"]
    tests = manifest["tests"]
    
    passed_count = 0
    total_count = len(tests)
    
    for test in tests:
        name = test["name"]
        test_input = test["input"]
        expected_output = test["expected_output"]
        
        try:
            # Run the command with the test input
            result = subprocess.run(
                [command, test_input],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            actual_output = result.stdout.strip()
            
            # Compare actual vs expected output
            if actual_output == expected_output:
                print(f"PASS: {name}")
                passed_count += 1
            else:
                print(f"FAIL: {name}")
        
        except Exception:
            print(f"FAIL: {name}")
    
    # Print summary
    print(f"{passed_count}/{total_count} tests passed")

if __name__ == "__main__":
    run_test_manifest()