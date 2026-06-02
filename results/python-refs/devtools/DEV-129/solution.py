import json
import sys

# Read JSON from stdin
input_data = json.loads(sys.stdin.read())

hook_type = input_data["hook_type"]
commands = input_data["commands"]

# Generate shell script
print("#!/bin/sh")
print("set -e")
print()
print(f"# {hook_type} hook")
for command in commands:
    print(command)
print()
print(f"echo '{hook_type} checks passed'")