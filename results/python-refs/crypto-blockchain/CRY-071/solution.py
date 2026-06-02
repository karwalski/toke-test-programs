import json
import sys

# Read initial state
initial_state = json.loads(input().strip())
current_state = initial_state["state"]
owner = initial_state["owner"]

# Read transitions
transitions = json.loads(input().strip())

# Process commands
try:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split()
        if len(parts) != 3 or parts[0] != "ACTION":
            continue
            
        caller = parts[1]
        action = parts[2]
        
        # Check if caller is owner
        if caller != owner:
            print("ERROR")
            sys.exit()
        
        # Check if transition is valid
        if current_state not in transitions:
            print("ERROR")
            sys.exit()
        
        if action not in transitions[current_state]:
            print("ERROR")
            sys.exit()
        
        # Execute transition
        current_state = transitions[current_state][action]
    
    # Output final state
    result = {"state": current_state, "owner": owner}
    print(json.dumps(result, separators=(',', ':')))
    
except:
    print("ERROR")