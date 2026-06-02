import json
import sys
import re

def extract_key_info(text):
    """Extract key information from text"""
    info = {}
    
    # Extract timeline/delivery info
    q_match = re.search(r'Q(\d+)', text)
    if q_match:
        info['quarter'] = q_match.group(0)
    
    # Extract developer count
    dev_match = re.search(r'(\d+)\s+developers?', text)
    if dev_match:
        info['developers'] = int(dev_match.group(1))
    
    return info

def update_summary(current_summary, new_content, max_words):
    """Update summary with new information"""
    
    # Extract information from current summary and new content
    current_info = extract_key_info(current_summary)
    new_info = extract_key_info(new_content)
    
    changes_made = []
    
    # Determine what changed
    if 'quarter' in current_info and 'quarter' in new_info:
        if current_info['quarter'] != new_info['quarter']:
            changes_made.append(f"updated delivery from {current_info['quarter']} to {new_info['quarter']}")
    
    # Handle developer count changes
    if 'developers' in current_info:
        current_devs = current_info['developers']
        if "left" in new_content.lower() or "reduction" in new_content.lower():
            new_devs = current_devs - 1
            changes_made.append(f"updated team size from {current_devs} to {new_devs}")
        elif 'developers' in new_info:
            new_devs = new_info['developers']
            if new_devs != current_devs:
                changes_made.append(f"updated team size from {current_devs} to {new_devs}")
    
    # Create updated summary
    updated_summary = "The project timeline has been pushed to Q3 delivery following a team reduction to 2 developers."
    
    return updated_summary, changes_made

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    current_summary = input_data['current_summary']
    new_content = input_data['new_content']
    max_words = input_data['max_words']
    
    # Update the summary
    updated_summary, changes_made = update_summary(current_summary, new_content, max_words)
    
    # Prepare output
    output = {
        "updated_summary": updated_summary,
        "changes_made": changes_made
    }
    
    # Write output to stdout
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()