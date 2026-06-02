import json
import sys

# Read input
inputs_line = input().strip()
outputs_line = input().strip()
fee_line = input().strip()

try:
    # Parse JSON inputs and outputs
    inputs = json.loads(inputs_line)
    outputs = json.loads(outputs_line)
    fee = float(fee_line)
    
    # Calculate total inputs and outputs
    total_inputs = sum(item['amount'] for item in inputs)
    total_outputs = sum(item['amount'] for item in outputs)
    
    # Check if amounts balance (inputs = outputs + fee)
    if abs(total_inputs - (total_outputs + fee)) < 1e-9:  # Use small epsilon for floating point comparison
        print(f"VALID: inputs={total_inputs:g}, outputs={total_outputs:g}, fee={fee:g}")
    else:
        print("INVALID: amounts do not balance")
        
except (json.JSONDecodeError, KeyError, ValueError) as e:
    print("INVALID: invalid input format")