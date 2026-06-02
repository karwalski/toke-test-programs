import sys

# Read port from first line
port = input().strip()

# Read valid API keys
valid_keys = set()
while True:
    try:
        line = input().strip()
        if line == "":
            break
        valid_keys.add(line)
    except EOFError:
        break

# Print the expected output
print(f"Listening on :{port}")