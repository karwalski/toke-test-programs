import sys, re
data = sys.stdin.read().split('\n', 1)
pattern = data[0]
text = data[1] if len(data) > 1 else ''
regex = re.compile(pattern)
for m in regex.finditer(text):
    if regex.groups >= 1:
        print(m.group(1))
    else:
        print(m.group(0))
