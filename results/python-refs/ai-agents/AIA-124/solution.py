import json
import sys

def validate_workflow_step(data):
    step = data["step"]
    step_id = step["id"]
    required_inputs = step["required_inputs"]
    available_outputs = data["available_outputs"]
    
    # Create a mapping of output field to source step
    output_to_source = {}
    for source_step, outputs in available_outputs.items():
        for output in outputs:
            output_to_source[output] = source_step
    
    # Check which inputs are satisfied and track sources
    missing = []
    sources = {}
    
    for required_input in required_inputs:
        if required_input in output_to_source:
            sources[required_input] = output_to_source[required_input]
        else:
            missing.append(required_input)
    
    satisfied = len(missing) == 0
    
    return {
        "satisfied": satisfied,
        "missing": missing,
        "sources": sources
    }

# Read input from stdin
input_data = json.load(sys.stdin)

# Process and validate
result = validate_workflow_step(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))