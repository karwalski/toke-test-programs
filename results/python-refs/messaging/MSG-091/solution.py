import json
import sys

def classify_message_priority():
    # Read input
    rules_line = input().strip()
    message_line = input().strip()
    
    # Parse JSON
    rules = json.loads(rules_line)
    message = json.loads(message_line)
    
    # Extract rules
    urgent_keywords = rules.get("urgent_keywords", [])
    high_priority_senders = rules.get("high_priority_senders", [])
    time_patterns = rules.get("time_patterns", [])
    
    # Extract message info
    sender = message.get("sender", "")
    text = message.get("text", "")
    
    # Analyze message
    reasons = []
    score = 0
    
    # Check sender priority
    if sender in high_priority_senders:
        reasons.append(f"high_priority_sender({sender})")
        score += 10
    
    # Check urgent keywords
    text_lower = text.lower()
    for keyword in urgent_keywords:
        if keyword.lower() in text_lower:
            reasons.append(f"urgent_keyword({keyword})")
            score += 15
    
    # Check time patterns
    for pattern in time_patterns:
        if pattern.lower() in text_lower:
            reasons.append(f"time_pattern({pattern})")
            score += 8
    
    # Determine priority level
    if score >= 20:
        priority = "CRITICAL"
    elif score >= 15:
        priority = "HIGH"
    elif score >= 5:
        priority = "NORMAL"
    else:
        priority = "LOW"
    
    # Output result
    print(priority)
    if reasons:
        print(f"reasons: {', '.join(reasons)}")

if __name__ == "__main__":
    classify_message_priority()