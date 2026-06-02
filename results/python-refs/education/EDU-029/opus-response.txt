import json
import sys

data = json.loads(sys.stdin.read().strip())
name = data["name"]
course = data["course"]
date = data["date"]
issuer = data["issuer"]

lines = []
lines.append("*" * 28)
lines.append("*  CERTIFICATE OF COMPLETION  *")
lines.append("*" + " " * 26 + "*")
for field in [name, course, date, issuer]:
    lines.append("*  " + field + " " * (26 - 2 - len(field)) + "  *")
lines.append("*" * 28)
print("\n".join(lines))