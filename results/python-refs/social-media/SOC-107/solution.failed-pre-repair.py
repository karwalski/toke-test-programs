import json
import sys
import re

def calculate_spam_score(content):
    spam_indicators = [
        r'\bbuy\b.*\bnow\b',
        r'\bcheap\b',
        r'\bfollowers\b',
        r'\bvisit\b.*\.com',
        r'\bfree\b.*\bmoney\b',
        r'\bclick\b.*\bhere\b',
        r'\bwin\b.*\bprize\b',
        r'\blimited\b.*\btime\b',
        r'\bact\b.*\bnow\b'
    ]
    
    content_lower = content.lower()
    matches = 0
    
    for pattern in spam_indicators:
        if re.search(pattern, content_lower, re.IGNORECASE):
            matches += 1
    
    # Base score calculation
    score = min(matches * 0.3, 1.0)
    
    # Boost for URLs
    if re.search(r'\w+\.\w+', content):
        score += 0.4
    
    # Boost for promotional language
    if re.search(r'\b(buy|cheap|now|visit)\b', content_lower):
        score += 0.25
    
    return min(score, 1.0)

def calculate_toxicity_score(content):
    toxic_words = [
        'hate', 'stupid', 'idiot', 'kill', 'die', 'moron',
        'loser', 'pathetic', 'worthless', 'disgusting'
    ]
    
    content_lower = content.lower()
    matches = sum(1 for word in toxic_words if word in content_lower)
    
    # Caps lock detection
    caps_ratio = sum(1 for c in content if c.isupper()) / max(len(content), 1)
    if caps_ratio > 0.7:
        matches += 1
    
    return min(matches * 0.2, 1.0)

def calculate_nsfw_score(content):
    nsfw_words = [
        'sex', 'porn', 'nude', 'naked', 'adult', 'xxx',
        'explicit', 'intimate', 'erotic'
    ]
    
    content_lower = content.lower()
    matches = sum(1 for word in nsfw_words if word in content_lower)
    
    return min(matches * 0.3, 1.0)

def determine_action(scores):
    max_score = max(scores.values())
    primary_reason = max(scores, key=scores.get)
    
    if max_score >= 0.8:
        return True, primary_reason, "hold_for_review"
    elif max_score >= 0.5:
        return True, primary_reason, "flag_for_review"
    else:
        return False, None, "approve"

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    if input_data.get("action") == "auto_moderate":
        content = input_data.get("content", "")
        
        scores = {
            "spam": round(calculate_spam_score(content), 2),
            "toxicity": round(calculate_toxicity_score(content), 1),
            "nsfw": round(calculate_nsfw_score(content), 1)
        }
        
        flagged, primary_reason, action = determine_action(scores)
        
        response = {
            "scores": scores,
            "flagged": flagged,
            "primary_reason": primary_reason,
            "action": action
        }
        
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()