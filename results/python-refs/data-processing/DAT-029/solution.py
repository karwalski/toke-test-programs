import sys
import re

data = sys.stdin.read()
if data.endswith('\n'):
    data = data[:-1]
lines = data.split('\n')

pattern = lines[0]
invert = False
data_start = 2

if len(lines) > 1 and lines[1].strip() == 'invert':
    invert = True

search_pattern = pattern
if search_pattern.startswith('^'):
    search_pattern = search_pattern[1:]

regex = re.compile(search_pattern)

results = []
for line in lines[data_start:]:
    matches = regex.search(line) is not None
    if matches != invert:
        results.append(line)

print('\n'.join(results))