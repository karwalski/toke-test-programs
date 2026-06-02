import json
import sys

def estimate_tokens(text):
    """Rough token estimation - approximately 1 token per 4 characters"""
    return len(text) // 4

def manage_sliding_window(data):
    messages = data['messages']
    max_tokens = data['max_tokens']
    current_token_count = data['current_token_count']
    
    # If we're under the limit, keep everything
    if current_token_count <= max_tokens:
        return {
            "kept_messages": list(range(len(messages))),
            "summarised": "",
            "new_token_count": current_token_count
        }
    
    # Always try to keep the last message (most recent)
    kept_indices = [len(messages) - 1]
    
    # Calculate tokens for the last message
    last_message = messages[-1]
    new_token_count = estimate_tokens(last_message['content'])
    
    # Work backwards to see what else we can keep
    for i in range(len(messages) - 2, -1, -1):
        message_tokens = estimate_tokens(messages[i]['content'])
        if new_token_count + message_tokens <= max_tokens:
            kept_indices.insert(0, i)
            new_token_count += message_tokens
        else:
            break
    
    # Create summary of discarded messages
    discarded_messages = messages[:kept_indices[0]] if kept_indices[0] > 0 else []
    
    summary_parts = []
    user_name = None
    user_company = None
    
    for msg in discarded_messages:
        content = msg['content'].lower()
        if msg['role'] == 'user':
            # Extract name
            if 'i am' in content or 'i\'m' in content:
                words = msg['content'].split()
                for i, word in enumerate(words):
                    if word.lower() in ['am', "i'm"] and i + 1 < len(words):
                        user_name = words[i + 1].rstrip(',.')
                        break
            
            # Extract company
            if 'work at' in content or 'works at' in content:
                words = msg['content'].split()
                for i, word in enumerate(words):
                    if word.lower() == 'at' and i + 1 < len(words):
                        company_parts = []
                        for j in range(i + 1, len(words)):
                            company_parts.append(words[j].rstrip(',.'))
                        user_company = ' '.join(company_parts)
                        break
    
    # Build summary
    if user_name and user_company:
        summary_parts.append(f"User is {user_name}, works at {user_company}")
    elif user_name:
        summary_parts.append(f"User is {user_name}")
    elif user_company:
        summary_parts.append(f"User works at {user_company}")
    
    # Add general interaction summary
    if any(msg['role'] == 'user' and any(greeting in msg['content'].lower() for greeting in ['hi', 'hello', 'hey']) for msg in discarded_messages):
        summary_parts.append("Previous greeting exchange")
    
    summarised = ". ".join(summary_parts) + "." if summary_parts else ""
    
    return {
        "kept_messages": kept_indices,
        "summarised": summarised,
        "new_token_count": new_token_count
    }

def main():
    input_data = json.loads(sys.stdin.read().strip())
    result = manage_sliding_window(input_data)
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()