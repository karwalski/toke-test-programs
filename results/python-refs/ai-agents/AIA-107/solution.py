import json
import sys

def generate_revised_instruction(data):
    original = data['original_instruction']
    agent_output = data['agent_output']
    feedback = data['feedback']
    
    # Analyze feedback to determine what improvements are needed
    changes_made = []
    revised_parts = [original]
    
    # Check for common feedback patterns and apply improvements
    feedback_lower = feedback.lower()
    
    if 'vague' in feedback_lower or 'generic' in feedback_lower:
        if 'specific' in feedback_lower:
            if 'features' in feedback_lower:
                revised_parts.append("that includes specific features")
                changes_made.append("Added requirement for specific features")
            
            if 'technical' in feedback_lower and ('detail' in feedback_lower or 'spec' in feedback_lower):
                revised_parts.append(", technical specifications")
                changes_made.append("Added requirement for technical specs")
        
        if 'use case' in feedback_lower:
            revised_parts.append(", and concrete use cases")
        elif len(revised_parts) > 1:
            revised_parts.append(", and concrete use cases")
        
        revised_parts.append(". Avoid generic superlatives.")
        changes_made.append("Added constraint against vague language")
    
    # Construct the revised instruction
    if len(revised_parts) > 1:
        revised_instruction = revised_parts[0] + "".join(revised_parts[1:])
    else:
        revised_instruction = original + " with more specific details based on the feedback."
        changes_made = ["Added requirement for more specific details"]
    
    return {
        "revised_instruction": revised_instruction,
        "changes_made": changes_made
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Generate the revised instruction
result = generate_revised_instruction(input_data)

# Output the result as JSON
print(json.dumps(result, separators=(',', ':')))