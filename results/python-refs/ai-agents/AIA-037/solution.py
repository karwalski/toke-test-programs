import json
import sys
import re

def classify_text(text, policies):
    violations = []
    
    # Define keyword patterns for each policy category
    policy_patterns = {
        'hate': [
            r'\b(hate|racist|nazi|kill all|exterminate|inferior race)\b',
            r'\b(die|death to|eliminate)\s+(jews|muslims|christians|blacks|whites|gays|lgbtq)\b'
        ],
        'violence': [
            r'\b(kill|murder|assassinate|shoot|stab|bomb|attack|destroy|hurt|harm|beat up)\b',
            r'\b(violence|violent|punch|kick|fight|war|weapon|gun|knife|explosive)\b'
        ],
        'harassment': [
            r'\b(stupid|idiot|moron|loser|freak|worthless|pathetic|disgusting)\b',
            r'\b(shut up|go die|kill yourself|you suck|hate you)\b'
        ],
        'sexual': [
            r'\b(sex|sexual|nude|naked|porn|orgasm|masturbate|rape|molest)\b',
            r'\b(penis|vagina|breast|genitals|erotic|seduce|horny)\b'
        ],
        'self-harm': [
            r'\b(suicide|kill myself|end my life|self harm|cut myself|overdose)\b',
            r'\b(want to die|better off dead|no point living|self injury)\b'
        ]
    }
    
    text_lower = text.lower()
    
    for policy in policies:
        if policy in policy_patterns:
            for pattern in policy_patterns[policy]:
                matches = list(re.finditer(pattern, text_lower, re.IGNORECASE))
                for match in matches:
                    violations.append({
                        "category": policy,
                        "severity": "high",
                        "span": [match.start(), match.end()]
                    })
    
    flagged = len(violations) > 0
    
    return {
        "flagged": flagged,
        "violations": violations
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())
text = input_data['text']
policies = input_data['policies']

# Classify the text
result = classify_text(text, policies)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))