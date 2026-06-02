import json
import sys

def solve_token_tracking():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    turns = input_data['turns']
    max_context = input_data['max_context']
    compression_threshold = input_data['compression_threshold']
    
    # Calculate total tokens
    total_tokens = sum(turn['token_count'] for turn in turns)
    
    # Calculate utilization
    utilisation = total_tokens / max_context
    
    # Determine action and evict count
    action = "none"
    evict_count = 0
    
    if utilisation >= compression_threshold:
        if total_tokens > max_context:
            # Need to evict tokens
            action = "evict"
            # Calculate how many turns to remove from the beginning
            tokens_to_remove = total_tokens - max_context
            current_tokens = 0
            for i, turn in enumerate(turns):
                current_tokens += turn['token_count']
                if current_tokens >= tokens_to_remove:
                    evict_count = i + 1
                    break
        else:
            # Need to compress but not evict
            action = "compress"
    
    # Create output
    result = {
        "total_tokens": total_tokens,
        "utilisation": utilisation,
        "action": action,
        "evict_count": evict_count
    }
    
    # Output JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    solve_token_tracking()