import sys
import json
import re

def analyze_prompt_injection(text):
    text_lower = text.lower()
    
    suspicious_patterns = []
    risk_score = 0
    
    # Pattern definitions with their risk scores
    patterns = [
        (r'\b(ignore|forget|disregard)\s+(all\s+)?(previous|prior|earlier)\s+(instructions?|commands?|prompts?)', 'ignore previous instructions', 3),
        (r'\byou\s+are\s+(now\s+)?(a|an|the)?\s*\w+', 'role reassignment', 3),
        (r'\bact\s+(as|like)\s+(a|an|the)?\s*\w+', 'role reassignment', 2),
        (r'\bpretend\s+(to\s+be|you\s+are)', 'role reassignment', 2),
        (r'\broleplay\s+(as|that)', 'role reassignment', 2),
        (r'\bsystem\s+(prompt|message|instruction)', 'system manipulation', 3),
        (r'\boverride\s+(previous|default|system)', 'override attempt', 3),
        (r'\breset\s+(to|your|the)', 'reset attempt', 2),
        (r'\bbegin\s+(new|fresh)\s+(session|conversation)', 'session manipulation', 2),
    ]
    
    # Check for patterns
    for pattern, name, score in patterns:
        if re.search(pattern, text_lower):
            if name not in suspicious_patterns:
                suspicious_patterns.append(name)
                risk_score += score
    
    # Determine risk level
    if risk_score >= 5:
        risk_level = "high"
    elif risk_score >= 3:
        risk_level = "medium"
    elif risk_score >= 1:
        risk_level = "low"
    else:
        risk_level = "none"
    
    # Determine if safe to process
    safe_to_process = risk_level in ["none", "low"]
    
    return {
        "risk_level": risk_level,
        "suspicious_patterns": suspicious_patterns,
        "safe_to_process": safe_to_process
    }

# Read input from stdin
input_text = sys.stdin.read().strip()

# Analyze the text
result = analyze_prompt_injection(input_text)

# Output JSON
print(json.dumps(result, separators=(',', ':')))