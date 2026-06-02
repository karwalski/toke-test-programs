import json
import csv
import sys

# Read input from stdin
input_data = sys.stdin.read()
messages = json.loads(input_data)

# Create CSV writer for stdout
writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

# Write header
writer.writerow(['id', 'sender', 'time', 'text'])

# Write message rows
for message in messages:
    writer.writerow([message['id'], message['sender'], message['time'], message['text']])