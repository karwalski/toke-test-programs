import json
import sys
from datetime import datetime

def parse_iso_date(iso_string):
    """Parse ISO date string to datetime object"""
    return datetime.fromisoformat(iso_string.replace('Z', '+00:00'))

def calculate_days_difference(reference_date, message_date):
    """Calculate days difference between reference and message date"""
    ref_dt = parse_iso_date(reference_date)
    msg_dt = parse_iso_date(message_date)
    return (ref_dt - msg_dt).days

def classify_message(days_old, policy):
    """Classify message based on age and retention policy"""
    if days_old < policy['hot_days']:
        return 'HOT'
    elif days_old < policy['warm_days']:
        return 'WARM'
    elif days_old < policy['cold_days']:
        return 'COLD'
    else:
        return 'PURGE'

def get_classification_description(classification, days_old, policy):
    """Get description for the classification"""
    if classification == 'HOT':
        return f"({days_old} days old, < {policy['hot_days']} days)"
    elif classification == 'WARM':
        return f"({days_old} days old, {policy['hot_days']}-{policy['warm_days']} days)"
    elif classification == 'COLD':
        return f"({days_old} days old, {policy['warm_days']}-{policy['cold_days']} days... exceeds, PURGE)"
    else:  # PURGE
        return f"({days_old} days old, > {policy['cold_days']} days)"

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse input
    policy = json.loads(lines[0])
    reference_date = lines[1]
    messages = json.loads(lines[2])
    
    # Process each message
    for message in messages:
        msg_id = message['id']
        msg_timestamp = message['timestamp']
        
        # Calculate age
        days_old = calculate_days_difference(reference_date, msg_timestamp)
        
        # Classify message
        classification = classify_message(days_old, policy)
        
        # Handle special case for COLD messages that exceed cold_days
        if classification == 'COLD' and days_old >= policy['cold_days']:
            classification = 'PURGE'
            description = get_classification_description('COLD', days_old, policy)
        else:
            description = get_classification_description(classification, days_old, policy)
        
        # Output result
        print(f"{msg_id}: {classification} {description}")

if __name__ == "__main__":
    main()