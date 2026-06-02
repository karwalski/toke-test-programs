import json
import sys

def calculate_workflow_progress(data):
    steps = data['steps']
    total_weight = sum(step['weight'] for step in steps)
    
    # Calculate completion percentage
    completed_weight = sum(step['weight'] for step in steps if step['status'] == 'done')
    completion_pct = (completed_weight / total_weight) * 100
    
    # Find current step (first running or pending step)
    current_step = None
    for step in steps:
        if step['status'] in ['running', 'pending']:
            current_step = step['id']
            break
    
    # Calculate ETA
    # First, calculate average duration per weight unit from completed steps
    completed_steps = [step for step in steps if step['status'] == 'done']
    if completed_steps:
        total_completed_duration = sum(step['duration_ms'] for step in completed_steps)
        total_completed_weight = sum(step['weight'] for step in completed_steps)
        avg_duration_per_weight = total_completed_duration / total_completed_weight
    else:
        # If no steps completed, use a default estimate
        avg_duration_per_weight = 1000  # Default 1000ms per weight unit
    
    # Calculate remaining weight (including running step)
    remaining_weight = sum(step['weight'] for step in steps if step['status'] in ['running', 'pending'])
    eta_ms = int(remaining_weight * avg_duration_per_weight)
    
    return {
        "completion_pct": completion_pct,
        "eta_ms": eta_ms,
        "current_step": current_step
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Calculate result
result = calculate_workflow_progress(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))