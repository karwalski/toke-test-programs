import json
import sys

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

# Parse state machine definition
state_machine = json.loads(lines[0])
initial_state = lines[1]
events = lines[2:]

# Build transition map
transitions = {}
for transition in state_machine["transitions"]:
    from_state = transition["from"]
    to_state = transition["to"]
    event = transition["event"]
    if from_state not in transitions:
        transitions[from_state] = {}
    transitions[from_state][event] = to_state

# Process events
current_state = initial_state
for event in events:
    if current_state in transitions and event in transitions[current_state]:
        next_state = transitions[current_state][event]
        print(f"{current_state} -> {next_state} ({event})")
        current_state = next_state
    else:
        print("INVALID TRANSITION")