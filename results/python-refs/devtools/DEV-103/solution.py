import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
specs = json.loads(input_data)

# Transform specs to mock server configuration
mocks = []
for spec in specs:
    mock = {
        "method": spec["method"],
        "path": spec["path"],
        "response": {
            "body": spec["response_body"],
            "status": spec["response_code"]
        }
    }
    mocks.append(mock)

# Create final configuration
config = {"mocks": mocks}

# Output to stdout
print(json.dumps(config, separators=(',', ':')))