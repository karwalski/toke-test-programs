import json
import re
import sys

input_data = json.loads(sys.stdin.read())

text = input_data['text']
patterns = input_data['patterns']

result = {}

for pattern_name, pattern_regex in patterns.items():
    # Handle over-escaped backslashes in input
    fixed = pattern_regex.replace('\\\\', '\\')
    matches = re.findall(fixed, text)
    result[pattern_name] = matches

print(json.dumps(result, separators=(',', ':')))