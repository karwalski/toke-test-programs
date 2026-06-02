import uuid
import sys

# Read input
try:
    line = input().strip()
    if line:
        n = int(line)
    else:
        n = 1
except EOFError:
    n = 1
except ValueError:
    n = 1

# Generate and print N UUIDs
for _ in range(n):
    print(str(uuid.uuid4()))