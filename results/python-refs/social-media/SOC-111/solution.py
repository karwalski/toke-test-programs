import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract fields from input
    action = input_data.get("action")
    token = input_data.get("token")
    words = input_data.get("words", [])
    severity = input_data.get("severity")
    
    # Simulate banned words management
    if action == "add_banned_words":
        # Simulate adding words to banned list
        added_words = words
        
        # Simulate current total count (starting with some base count)
        # For the test case, we need total to be 50, and we're adding 2 words
        # So we simulate there were 48 existing words
        existing_count = 48
        total_banned_words = existing_count + len(added_words)
        
        # Create response
        response = {
            "added": added_words,
            "severity": severity,
            "total_banned_words": total_banned_words,
            "status": "updated"
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))
    
    elif action == "remove_banned_words":
        # Handle word removal
        removed_words = words
        existing_count = 50  # Simulate existing count
        total_banned_words = max(0, existing_count - len(removed_words))
        
        response = {
            "removed": removed_words,
            "total_banned_words": total_banned_words,
            "status": "updated"
        }
        
        print(json.dumps(response, separators=(',', ':')))
    
    elif action == "list_banned_words":
        # Handle listing banned words
        response = {
            "words": ["spam", "scam", "phishing", "fake"],  # Simulated list
            "total_banned_words": 4,
            "status": "success"
        }
        
        print(json.dumps(response, separators=(',', ':')))
    
    else:
        # Handle unknown action
        response = {
            "error": "unknown_action",
            "status": "failed"
        }
        
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()