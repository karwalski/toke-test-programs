import json
import sys

def select_next_task():
    # Read input from stdin
    input_data = json.load(sys.stdin)
    
    backlog = input_data['backlog']
    now_ms = input_data['now_ms']
    completed_tasks = set(input_data['completed_tasks'])
    
    # Filter out completed tasks and tasks with unmet dependencies
    available_tasks = []
    for task in backlog:
        if task['id'] not in completed_tasks:
            # Check if all dependencies are completed
            dependencies_met = all(dep in completed_tasks for dep in task['depends_on'])
            if dependencies_met:
                available_tasks.append(task)
    
    if not available_tasks:
        # No available tasks
        result = {
            "next_task": None,
            "reasoning": "No available tasks",
            "urgency_score": 0.0
        }
        print(json.dumps(result, separators=(',', ':')))
        return
    
    # Calculate scores for each available task
    best_task = None
    best_score = -1
    best_reasoning = ""
    best_urgency = 0.0
    
    for task in available_tasks:
        task_id = task['id']
        priority = task['priority']
        deadline_ms = task['deadline_ms']
        estimated_duration_ms = task['estimated_duration_ms']
        
        # Calculate slack time (how much time we have before we must start)
        slack_time = deadline_ms - now_ms - estimated_duration_ms
        
        # Calculate urgency score based on slack time
        if slack_time <= 0:
            urgency_score = 1.0
        else:
            # Normalize urgency score based on slack relative to duration
            max_reasonable_slack = estimated_duration_ms * 2  # Arbitrary reasonable slack
            urgency_score = max(0.0, 1.0 - (slack_time / max_reasonable_slack))
        
        # Combine urgency with priority (higher priority = lower priority number)
        # Invert priority so higher numbers are better
        priority_score = 1.0 / priority if priority > 0 else 1.0
        
        # Overall score combines urgency and priority
        overall_score = urgency_score * 0.7 + priority_score * 0.3
        
        if overall_score > best_score:
            best_task = task_id
            best_score = overall_score
            best_urgency = urgency_score
            
            # Generate reasoning
            if slack_time <= 0:
                best_reasoning = f"Task past deadline, must start immediately"
            elif slack_time < estimated_duration_ms:
                best_reasoning = f"Closest deadline ({deadline_ms}ms) with only {slack_time}ms slack, must start now"
            else:
                best_reasoning = f"Best combination of urgency (deadline {deadline_ms}ms) and priority ({priority})"
    
    result = {
        "next_task": best_task,
        "reasoning": best_reasoning,
        "urgency_score": round(best_urgency, 2)
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    select_next_task()