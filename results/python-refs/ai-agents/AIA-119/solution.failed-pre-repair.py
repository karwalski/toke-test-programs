import json
import sys

def evaluate_condition(condition, context):
    """Evaluate a condition string against the context variables."""
    # Replace variable names with their values from context
    condition_expr = condition
    
    # Replace logical operators
    condition_expr = condition_expr.replace(" AND ", " and ")
    condition_expr = condition_expr.replace(" OR ", " or ")
    condition_expr = condition_expr.replace(" NOT ", " not ")
    
    # Replace variables with their values
    for var, value in context.items():
        if isinstance(value, str):
            condition_expr = condition_expr.replace(var, f'"{value}"')
        else:
            condition_expr = condition_expr.replace(var, str(value))
    
    try:
        # Evaluate the expression safely
        return eval(condition_expr)
    except:
        return False

def solve_workflow_branch(data):
    """Determine which branch to take based on conditions."""
    context = data["context"]
    branches = data["branches"]
    
    # Sort branches by priority (lower number = higher priority)
    sorted_branches = sorted(branches, key=lambda x: x["priority"])
    
    # Check each branch condition
    for branch in sorted_branches:
        condition = branch["condition"]
        target = branch["target"]
        
        if evaluate_condition(condition, context):
            return {
                "selected_branch": target,
                "condition_met": condition,
                "fallback": False
            }
    
    # If no condition matches, use the first branch as fallback
    if branches:
        first_branch = sorted_branches[0]
        return {
            "selected_branch": first_branch["target"],
            "condition_met": first_branch["condition"],
            "fallback": True
        }
    
    # No branches available
    return {
        "selected_branch": None,
        "condition_met": None,
        "fallback": True
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Process the workflow branch decision
result = solve_workflow_branch(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))