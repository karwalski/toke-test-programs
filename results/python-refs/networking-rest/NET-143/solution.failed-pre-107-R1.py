import sys

# Read host
host = input().strip()

# Read port
port = int(input().strip())

# Read messages until blank line
messages = []
while True:
    try:
        line = input()
        if line == "":
            break
        messages.append(line)
    except EOFError:
        break

# Simulate TCP connection and responses
# Since we need to simulate the behavior, we'll echo back each message
for message in messages:
    print(message)

print("Connection closed")