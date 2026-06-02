import json
import sys

def generate_dashboard():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())
    files = input_data["files"]
    
    # Calculate basic metrics
    num_files = len(files)
    total_lines = sum(file["lines"] for file in files)
    avg_complexity = sum(file["complexity"] for file in files) / num_files
    max_complexity = max(file["complexity"] for file in files)
    avg_coverage = sum(file["coverage_pct"] for file in files) / num_files
    files_with_tests = sum(1 for file in files if file["test_exists"])
    
    # Identify risk files (coverage < 80% or no tests)
    risk_files = []
    for file in files:
        if file["coverage_pct"] < 80 or not file["test_exists"]:
            risk_info = f"  {file['path']} (coverage: {file['coverage_pct']}%"
            if not file["test_exists"]:
                risk_info += ", no tests"
            risk_info += ")"
            risk_files.append(risk_info)
    
    # Generate output
    print("Code Metrics Dashboard")
    print(f"Files: {num_files} | Total lines: {total_lines}")
    print(f"Avg complexity: {avg_complexity} | Max complexity: {max_complexity}")
    print(f"Avg coverage: {avg_coverage}% | Files with tests: {files_with_tests}/{num_files}")
    print("Risk files:")
    for risk_file in risk_files:
        print(risk_file)

if __name__ == "__main__":
    generate_dashboard()