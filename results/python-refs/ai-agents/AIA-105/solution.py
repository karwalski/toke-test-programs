import json
import sys

def solve_work_distribution():
    # Read input from stdin
    input_data = json.load(sys.stdin)
    work_items = input_data['work_items']
    agents = input_data['agents']
    
    # Initialize result dictionary
    result = {agent['id']: [] for agent in agents}
    
    # Create a list to track remaining capacity for each agent
    agent_capacity = {agent['id']: agent['capacity'] for agent in agents}
    
    # Sort work items by complexity (descending) for better distribution
    work_items_sorted = sorted(work_items, key=lambda x: x['complexity'], reverse=True)
    
    # Distribute work items
    for work_item in work_items_sorted:
        best_agent = None
        best_score = -1
        
        for agent in agents:
            agent_id = agent['id']
            
            # Check if agent has capacity
            if agent_capacity[agent_id] < work_item['complexity']:
                continue
                
            # Check if agent has the right specialty
            if work_item['type'] not in agent['specialties']:
                continue
            
            # Calculate score based on remaining capacity (prefer agents with more remaining capacity)
            score = agent_capacity[agent_id] - work_item['complexity']
            
            if best_agent is None or score > best_score:
                best_agent = agent_id
                best_score = score
        
        # Assign work item to best agent
        if best_agent:
            result[best_agent].append(work_item['id'])
            agent_capacity[best_agent] -= work_item['complexity']
    
    # Output result as JSON
    print(json.dumps(result, separators=(',', ':')))

solve_work_distribution()