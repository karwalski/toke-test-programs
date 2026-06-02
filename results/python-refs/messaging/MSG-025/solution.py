import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
messages = json.loads(input_data)

# Sort messages by sequence number
messages.sort(key=lambda x: x['seq'])

# Print messages in order
for msg in messages:
    print(f"{msg['seq']}: {msg['text']}")

# Detect gaps
if not messages:
    print("gaps: none")
else:
    gaps = []
    expected_seq = messages[0]['seq']
    
    for msg in messages:
        while expected_seq < msg['seq']:
            gaps.append(expected_seq)
            expected_seq += 1
        expected_seq = msg['seq'] + 1
    
    if gaps:
        print(f"gaps: {', '.join(map(str, gaps))}")
    else:
        print("gaps: none")