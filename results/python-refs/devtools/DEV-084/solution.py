import json
import sys

def validate_iam_policy(policy):
    risks = []
    
    # Parse the policy
    try:
        policy_doc = json.loads(policy)
    except json.JSONDecodeError:
        risks.append("RISK: Invalid JSON format")
        return risks
    
    # Check if Statement exists
    if "Statement" not in policy_doc:
        risks.append("RISK: No Statement found in policy")
        return risks
    
    statements = policy_doc["Statement"]
    if not isinstance(statements, list):
        statements = [statements]
    
    # Check each statement
    for statement in statements:
        if not isinstance(statement, dict):
            continue
            
        # Check for wildcard actions
        if "Action" in statement:
            actions = statement["Action"]
            if not isinstance(actions, list):
                actions = [actions]
            
            for action in actions:
                if action == "*":
                    risks.append("RISK: Statement allows all actions (*)")
                    break
        
        # Check for wildcard resources
        if "Resource" in statement:
            resources = statement["Resource"]
            if not isinstance(resources, list):
                resources = [resources]
            
            for resource in resources:
                if resource == "*":
                    risks.append("RISK: Statement allows all resources (*)")
                    break
    
    return risks

# Read from stdin
policy_input = sys.stdin.read().strip()

# Validate the policy
risks = validate_iam_policy(policy_input)

# Output results
if risks:
    for risk in risks:
        print(risk)
else:
    print("SECURE")