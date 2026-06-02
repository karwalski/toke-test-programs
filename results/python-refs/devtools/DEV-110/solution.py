import json
import sys

# Read input
lines = sys.stdin.read().strip().split('\n')
test_mapping = json.loads(lines[0])
changed_files = lines[1].split()

# Find tests that should run
tests_to_run = set()

for test_name, test_files in test_mapping.items():
    for changed_file in changed_files:
        if changed_file in test_files:
            tests_to_run.add(test_name)
            break

# Sort and output
for test in sorted(tests_to_run):
    print(test)