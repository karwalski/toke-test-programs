import json
import sys

def aggregate_outputs(data):
    task_type = data['task_type']
    agent_outputs = data['agent_outputs']
    
    # Sort by order
    sorted_outputs = sorted(agent_outputs, key=lambda x: x['order'])
    
    # Build aggregated result
    result_parts = []
    contributors = []
    
    for output in sorted_outputs:
        section_title = output['section'].title()
        content = output['content']
        result_parts.append(f"## {section_title}\n{content}")
        contributors.append(output['agent_id'])
    
    aggregated_result = "\n\n".join(result_parts)
    
    # Calculate completeness (assuming 1.0 if we have any outputs)
    completeness = 1.0 if agent_outputs else 0.0
    
    return {
        "aggregated_result": aggregated_result,
        "contributors": contributors,
        "completeness": completeness
    }

# Read from stdin
input_data = json.load(sys.stdin)

# Process and output
result = aggregate_outputs(input_data)
print(json.dumps(result, separators=(',', ':')))