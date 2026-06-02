import json
import re
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read())

text = input_data['text']
patterns = input_data['patterns']

result = {}

# For each pattern, find all matches in the text
for pattern_name, pattern_regex in patterns.items():
    matches = re.findall(pattern_regex, text)
    result[pattern_name] = matches

# Output the result as JSON
print(json.dumps(result, separators=(',', ':')))