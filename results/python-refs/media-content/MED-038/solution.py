import json
import sys

input_json = sys.stdin.read().strip()
data = json.loads(input_json)
pretty_json = json.dumps(data, indent=2)
print(pretty_json)