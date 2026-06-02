import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract the words from the input
words = input_data.get("words", [])

# Create the response
response = {
    "muted_words": words,
    "total": len(words),
    "status": "updated"
}

# Output the response as JSON
print(json.dumps(response, separators=(',', ':')))