import sys

print("<dl>")
for line in sys.stdin:
    line = line.strip()
    if line:
        term, definition = line.split(": ", 1)
        print(f"  <dt>{term}</dt>")
        print(f"  <dd>{definition}</dd>")
print("</dl>")