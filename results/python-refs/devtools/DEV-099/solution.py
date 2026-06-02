import json
import sys
from collections import defaultdict

# Read input from stdin
input_data = sys.stdin.read().strip()
lint_findings = json.loads(input_data)

# Count violations by rule and by file
rule_counts = defaultdict(int)
file_counts = defaultdict(int)
total_violations = 0

for finding in lint_findings:
    rule_counts[finding['rule_id']] += 1
    file_counts[finding['file']] += 1
    total_violations += 1

# Generate output
print("Style Report")
print()
print("By rule:")
for rule in sorted(rule_counts.keys()):
    print(f"  {rule}: {rule_counts[rule]} violations")
print()
print("By file:")
for file in sorted(file_counts.keys()):
    print(f"  {file}: {file_counts[file]} violations")
print()
print(f"Total: {total_violations} violations")