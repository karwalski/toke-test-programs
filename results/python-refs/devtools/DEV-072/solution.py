import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
test_runs = json.loads(input_data)

# Count passes and fails for each test
test_results = {}
for run in test_runs:
    test_name = run["test_name"]
    status = run["status"]
    
    if test_name not in test_results:
        test_results[test_name] = {"passes": 0, "fails": 0}
    
    if status == "pass":
        test_results[test_name]["passes"] += 1
    elif status == "fail":
        test_results[test_name]["fails"] += 1

# Find flaky tests (tests with both passes and fails)
flaky_tests = []
for test_name, results in test_results.items():
    if results["passes"] > 0 and results["fails"] > 0:
        flaky_tests.append((test_name, results["passes"], results["fails"]))

# Sort by fail count descending
flaky_tests.sort(key=lambda x: x[2], reverse=True)

# Output results
for test_name, passes, fails in flaky_tests:
    print(f"FLAKY: {test_name} ({passes} passes, {fails} fails)")