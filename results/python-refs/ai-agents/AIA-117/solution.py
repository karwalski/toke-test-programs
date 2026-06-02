import json
import sys

def calculate_state_diff(old_state, new_state):
    additions = {}
    deletions = []
    modifications = {}
    
    # Find additions and modifications
    for key, new_value in new_state.items():
        if key not in old_state:
            additions[key] = new_value
        elif old_state[key] != new_value:
            modifications[key] = {"old": old_state[key], "new": new_value}
    
    # Find deletions
    for key in old_state:
        if key not in new_state:
            deletions.append(key)
    
    return {
        "additions": additions,
        "deletions": deletions,
        "modifications": modifications
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())
old_state = input_data["old_state"]
new_state = input_data["new_state"]

# Calculate diff
result = calculate_state_diff(old_state, new_state)

# Output result to stdout
print(json.dumps(result, separators=(',', ':')))