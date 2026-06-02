import json
import sys

# Read JSON from stdin
input_json = sys.stdin.read()

# Parse and reformat without whitespace
data = json.loads(input_json)
compact_json = json.dumps(data, separators=(',', ':'))

# Write to stdout
print(compact_json)