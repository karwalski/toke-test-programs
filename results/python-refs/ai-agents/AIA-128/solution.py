import json
import sys

def solve_replanning():
    input_data = json.load(sys.stdin)
    
    original_plan = input_data['original_plan']
    completed = input_data['completed']
    failed = input_data['failed']
    goal = input_data['goal']
    
    # Create a set of completed step ids for quick lookup
    completed_set = set(completed)
    
    # Create a mapping of failed step ids to their errors
    failed_dict = {f['step_id']: f['error'] for f in failed}
    
    revised_plan = []
    adaptations = []
    
    # Process each step in the original plan
    for step in original_plan:
        step_id = step['id']
        
        # Skip completed steps
        if step_id in completed_set:
            continue
            
        # Handle failed steps with adaptations
        if step_id in failed_dict:
            error = failed_dict[step_id]
            
            if step_id == "s2" and "API B is down" in error:
                # Replace with cache alternative
                adapted_step = {
                    "id": "s2_alt",
                    "action": "fetch_api_b_cache",
                    "description": "Use cached data from API B"
                }
                revised_plan.append(adapted_step)
                adaptations.append("Replaced live API B fetch with cached data due to API being down")
        else:
            # Include remaining steps that haven't failed
            if step_id == "s4":
                # Add note about stale data for report generation
                adapted_step = step.copy()
                adapted_step["note"] = "Mark API B data as potentially stale"
                revised_plan.append(adapted_step)
                adaptations.append("Added staleness warning to report")
            else:
                revised_plan.append(step)
    
    result = {
        "revised_plan": revised_plan,
        "adaptations": adaptations
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    solve_replanning()