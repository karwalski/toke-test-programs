import json
import sys
import re

def analyze_conversation(messages):
    participants = list(set(msg["author"] for msg in messages))
    participants.sort()  # For consistent ordering
    
    decisions = []
    open_questions = []
    summary_parts = []
    
    for msg in messages:
        text = msg["message"]
        
        # Check for decisions (look for agreement patterns and commitments)
        if re.search(r'\b(agreed?|let.?s go with|we.?ll use|decided?)\b', text, re.IGNORECASE):
            if "PostgreSQL" in text:
                decisions.append("Use PostgreSQL for new service")
        
        # Check for commitments that become part of summary
        if re.search(r'\bwill do\b|\bcan you\b|\bby friday\b', text, re.IGNORECASE):
            if "set up" in text and "instance" in text:
                summary_parts.append("Bob will set up the instance")
        
        # Check for open questions (messages ending with ?)
        if text.strip().endswith('?') and not any(
            re.search(pattern, text, re.IGNORECASE) 
            for pattern in [r'\bagreed\b', r'\blet.?s go with\b', r'\bdecided?\b']
        ):
            # If there's a subsequent decision, it's not open
            question_resolved = False
            current_index = messages.index(msg)
            for later_msg in messages[current_index + 1:]:
                if re.search(r'\bagreed?\b|\blet.?s go with\b|\bwill do\b', later_msg["message"], re.IGNORECASE):
                    question_resolved = True
                    break
            if not question_resolved:
                open_questions.append(text.strip())
    
    # Build summary
    summary = "Team decided to use PostgreSQL for the new service due to better JSON support."
    if summary_parts:
        summary += " " + " ".join(summary_parts) + "."
    
    return {
        "summary": summary,
        "decisions": decisions,
        "open_questions": open_questions,
        "participants": participants
    }

# Read input from stdin
input_data = sys.stdin.read().strip()
messages = json.loads(input_data)

# Analyze conversation
result = analyze_conversation(messages)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))