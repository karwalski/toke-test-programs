import re
import json
import sys

lines = sys.stdin.read().strip().split('\n')
pattern = lines[0]
regex = re.compile(pattern)

for line in lines[1:]:
    match = regex.match(line)
    if match:
        result = match.groupdict()
        print(json.dumps(result, separators=(',', ':')))