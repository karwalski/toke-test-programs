import json
import sys

data = json.load(sys.stdin)
print(json.dumps(data, indent=2))