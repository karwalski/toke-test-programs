import json
import sys

def break_down_goal(goal, available_actions):
    # Define common goal patterns and their step sequences
    goal_patterns = {
        "python web project": [
            {
                "step": 1,
                "action": "create_directory",
                "success_criteria": "Project directory structure exists",
                "fallback": "Check permissions and retry"
            },
            {
                "step": 2,
                "action": "write_file",
                "success_criteria": "requirements.txt and main app file created",
                "fallback": "Verify disk space"
            },
            {
                "step": 3,
                "action": "run_command",
                "success_criteria": "Virtual env created and dependencies installed",
                "fallback": "Check Python version"
            },
            {
                "step": 4,
                "action": "write_file",
                "success_criteria": "Test files created with passing tests",
                "fallback": "Review test framework docs"
            },
            {
                "step": 5,
                "action": "configure_service",
                "success_criteria": "CI pipeline configured and running",
                "fallback": "Check service credentials"
            }
        ]
    }
    
    # Check if goal matches known patterns
    goal_lower = goal.lower()
    if "python" in goal_lower and "web" in goal_lower and "project" in goal_lower:
        base_plan = goal_patterns["python web project"]
        # Filter steps based on available actions
        filtered_plan = []
        for step in base_plan:
            if step["action"] in available_actions:
                filtered_plan.append(step)
        
        # Renumber steps
        for i, step in enumerate(filtered_plan):
            step["step"] = i + 1
            
        return filtered_plan
    
    # Default generic breakdown
    plan = []
    step_num = 1
    
    if "create_directory" in available_actions:
        plan.append({
            "step": step_num,
            "action": "create_directory",
            "success_criteria": "Required directories created",
            "fallback": "Check permissions"
        })
        step_num += 1
    
    if "write_file" in available_actions:
        plan.append({
            "step": step_num,
            "action": "write_file",
            "success_criteria": "Configuration files written",
            "fallback": "Check disk space"
        })
        step_num += 1
    
    if "run_command" in available_actions:
        plan.append({
            "step": step_num,
            "action": "run_command",
            "success_criteria": "Commands executed successfully",
            "fallback": "Check dependencies"
        })
        step_num += 1
    
    if "configure_service" in available_actions:
        plan.append({
            "step": step_num,
            "action": "configure_service",
            "success_criteria": "Services configured",
            "fallback": "Check service status"
        })
    
    return plan

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    data = json.loads(input_data)
    
    goal = data["goal"]
    available_actions = data["available_actions"]
    
    # Generate plan
    plan = break_down_goal(goal, available_actions)
    
    # Create output
    output = {"plan": plan}
    
    # Write to stdout
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()