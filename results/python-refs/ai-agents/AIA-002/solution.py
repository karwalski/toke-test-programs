import json
import sys

def parse_query_and_create_plan(data):
    tools = {tool['name']: tool['params'] for tool in data['tools']}
    query = data['query'].lower()
    
    plan = []
    step_id = 1
    
    # Step 1: Search for articles about rust programming
    if 'search' in tools:
        plan.append({
            "step_id": step_id,
            "tool": "search",
            "arguments": {"query": "rust programming"},
            "depends_on": []
        })
        step_id += 1
    
    # Step 2: Summarise the search results
    if 'summarise' in tools and len(plan) > 0:
        plan.append({
            "step_id": step_id,
            "tool": "summarise",
            "arguments": {"text": "$1.result"},
            "depends_on": [1]
        })
        step_id += 1
    
    # Step 3: Email the summary
    if 'email' in tools and len(plan) > 1:
        plan.append({
            "step_id": step_id,
            "tool": "email",
            "arguments": {"to": "bob@example.com", "body": "$2.result"},
            "depends_on": [2]
        })
    
    return plan

# Read input from stdin
input_data = json.loads(sys.stdin.read())

# Generate execution plan
execution_plan = parse_query_and_create_plan(input_data)

# Output as JSON
print(json.dumps(execution_plan, separators=(',', ':')))