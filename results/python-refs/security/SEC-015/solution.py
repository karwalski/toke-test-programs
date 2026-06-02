import json
import sys
from collections import defaultdict

def main():
    # Read JSON from stdin
    input_data = sys.stdin.read().strip()
    findings = json.loads(input_data)
    
    # Check if any finding has high severity
    for finding in findings:
        if finding.get("severity", "").lower() == "high":
            print("CRITICAL")
            return
    
    # If no high severity findings, check for other severities
    severities = [finding.get("severity", "").lower() for finding in findings]
    
    if "medium" in severities:
        print("MEDIUM")
    elif "low" in severities:
        print("LOW")
    elif findings:  # Has findings but no recognized severity
        print("LOW")
    else:
        print("CLEAN")

if __name__ == "__main__":
    main()