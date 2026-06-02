import json
import sys

def analyze_token_usage(data):
    conversations = data['conversations']
    
    # Calculate summary statistics
    total_input_tokens = sum(conv['total_input_tokens'] for conv in conversations)
    total_output_tokens = sum(conv['total_output_tokens'] for conv in conversations)
    total_cost = sum(conv['cost'] for conv in conversations)
    
    num_conversations = len(conversations)
    avg_input_tokens = total_input_tokens // num_conversations
    avg_output_tokens = total_output_tokens // num_conversations
    
    # Identify outliers (conversations using 2x+ average tokens)
    outliers = []
    recommendations = []
    
    for conv in conversations:
        input_ratio = conv['total_input_tokens'] / avg_input_tokens
        output_ratio = conv['total_output_tokens'] / avg_output_tokens
        
        if input_ratio >= 2.0 or output_ratio >= 2.0:
            outliers.append(conv['id'])
            
            if input_ratio >= 2.0:
                recommendations.append(f"Conversation {conv['id']} uses {conv['total_input_tokens']} input tokens ({input_ratio:.1f}x average) - consider context compression")
            elif output_ratio >= 2.0:
                recommendations.append(f"Conversation {conv['id']} uses {conv['total_output_tokens']} output tokens ({output_ratio:.1f}x average) - consider response optimization")
    
    # Build result
    result = {
        "summary": {
            "avg_input_tokens": avg_input_tokens,
            "avg_output_tokens": avg_output_tokens,
            "total_cost": total_cost
        },
        "outliers": outliers,
        "recommendations": recommendations
    }
    
    return result

# Read input from stdin
input_data = json.loads(sys.stdin.read())

# Analyze and output result
result = analyze_token_usage(input_data)
print(json.dumps(result, separators=(',', ':')))