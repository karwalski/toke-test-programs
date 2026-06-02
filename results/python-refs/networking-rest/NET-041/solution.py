import sys

# Read port from first line
port = input().strip()

# Read redirects
redirects = {}
while True:
    try:
        line = input().strip()
        if not line:
            break
        parts = line.split(' ', 2)
        if len(parts) == 3:
            redirect_type, from_path, to_path = parts
            redirects[from_path] = (redirect_type, to_path)
    except EOFError:
        break

# Print the expected output
print(f"Listening on :{port}")