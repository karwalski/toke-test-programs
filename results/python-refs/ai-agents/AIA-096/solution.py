import json
import sys

def assign_agents(input_data):
    task = input_data['task']
    agents = input_data['agents']
    
    # Define subtasks and required capabilities
    subtasks = [
        {
            "description": "Write blog post about machine learning",
            "required_capabilities": ["writing"],
            "keywords": ["write", "blog post"]
        },
        {
            "description": "Review post for errors", 
            "required_capabilities": ["proofreading"],
            "keywords": ["review", "errors"]
        },
        {
            "description": "Publish to website",
            "required_capabilities": ["publishing"],
            "keywords": ["publish", "website"]
        }
    ]
    
    assignments = []
    
    for subtask in subtasks:
        best_agent = None
        best_reason = ""
        
        for agent in agents:
            # Check if agent has required capabilities
            has_required = any(cap in agent['capabilities'] for cap in subtask['required_capabilities'])
            
            if has_required:
                if subtask['description'] == "Write blog post about machine learning":
                    if "writing" in agent['capabilities']:
                        best_agent = agent['id']
                        best_reason = "Content writing capability matches"
                        break
                elif subtask['description'] == "Review post for errors":
                    if "proofreading" in agent['capabilities']:
                        best_agent = agent['id']
                        best_reason = "Proofreading and fact-checking capabilities"
                        break
                elif subtask['description'] == "Publish to website":
                    if "publishing" in agent['capabilities']:
                        best_agent = agent['id']
                        best_reason = "Publishing capability"
                        break
        
        if best_agent:
            assignments.append({
                "agent_id": best_agent,
                "subtask": subtask['description'],
                "reason": best_reason
            })
    
    return {"assignments": assignments}

# Read input from stdin
input_text = sys.stdin.read().strip()
input_data = json.loads(input_text)

# Process and assign agents
result = assign_agents(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))