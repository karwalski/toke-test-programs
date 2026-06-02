import json
import sys

def solve_workflow_transition(input_data):
    current_state = input_data["current_state"]
    event = input_data["event"]
    transitions = input_data["transitions"]
    context = input_data["context"]
    
    # Find matching transition
    for transition in transitions:
        if (transition["from"] == current_state and 
            transition["event"] == event):
            
            # Check guard condition if present
            if "guard" in transition:
                # For this simple implementation, we'll assume guards are basic
                # In a real system, you'd evaluate the guard expression
                pass
            
            return {
                "next_state": transition["to"],
                "transition_taken": True,
                "side_effects": []
            }
    
    # No matching transition found
    return {
        "next_state": current_state,
        "transition_taken": False,
        "side_effects": []
    }

# Read input from stdin
input_json = sys.stdin.read().strip()
input_data = json.loads(input_json)

# Process the workflow transition
result = solve_workflow_transition(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))