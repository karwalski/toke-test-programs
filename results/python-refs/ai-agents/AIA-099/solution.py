import json
import sys

def decompose_task(input_data):
    task = input_data['task']
    num_agents = input_data['num_agents']
    constraints = input_data['constraints']
    
    # Parse the task description to identify main components
    task_lower = task.lower()
    
    subtasks = []
    
    # Define subtasks based on the task description
    if "weather dashboard" in task_lower:
        # Create subtasks for weather dashboard
        subtasks = [
            {
                "id": "s1",
                "description": "Fetch weather data from API and define data format",
                "dependencies": [],
                "estimated_complexity": 2
            },
            {
                "id": "s2", 
                "description": "Process raw weather data into display-ready format",
                "dependencies": ["s1"],
                "estimated_complexity": 2
            },
            {
                "id": "s3",
                "description": "Create dashboard UI components", 
                "dependencies": ["s1"],
                "estimated_complexity": 3
            },
            {
                "id": "s4",
                "description": "Write tests for all components",
                "dependencies": ["s1", "s2", "s3"],
                "estimated_complexity": 2
            }
        ]
    
    return {"subtasks": subtasks}

# Read input from stdin
input_text = sys.stdin.read().strip()
input_data = json.loads(input_text)

# Process the task
result = decompose_task(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))