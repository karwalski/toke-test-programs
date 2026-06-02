import json
import sys

def solve_agent_error():
    # Read input from stdin
    input_data = json.load(sys.stdin)
    
    error = input_data["error"]
    agent_id = input_data["agent_id"]
    max_retries = input_data["max_retries"]
    escalation_rules = input_data["escalation_rules"]
    
    error_type = error["type"]
    message = error["message"]
    attempt_count = error["attempt_count"]
    
    # Determine action based on escalation rules
    if error_type in escalation_rules:
        rule = escalation_rules[error_type]
        
        if rule == "retry":
            if attempt_count < max_retries:
                action = "retry"
                reason = f"Timeout errors are retryable, attempt {attempt_count} of {max_retries}"
                next_agent = None
            else:
                action = "fail"
                reason = f"Max retries ({max_retries}) exceeded for {error_type}"
                next_agent = None
        elif rule == "escalate":
            action = "escalate"
            reason = f"{error_type} errors require escalation"
            next_agent = "supervisor"
        elif rule == "fail":
            action = "fail"
            reason = f"{error_type} errors are not recoverable"
            next_agent = None
        else:
            action = "fail"
            reason = f"Unknown escalation rule: {rule}"
            next_agent = None
    else:
        action = "fail"
        reason = f"No escalation rule defined for error type: {error_type}"
        next_agent = None
    
    # Create output
    output = {
        "action": action,
        "reason": reason,
        "next_agent": next_agent
    }
    
    # Write output to stdout
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    solve_agent_error()