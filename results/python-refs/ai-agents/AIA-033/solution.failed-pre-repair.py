import json
import sys
import re

def analyze_spam(subject, body):
    factors = []
    confidence = 0.0
    
    # Combine subject and body for analysis
    text = (subject + " " + body).lower()
    
    # Check for urgency language
    urgency_words = ['urgent', 'immediate', 'now', 'hurry', 'limited time', 'act now', 'expires']
    if any(word in text for word in urgency_words):
        factors.append("urgency language")
        confidence += 0.25
    
    # Check for monetary claims
    money_patterns = [r'\$[\d,]+', r'won.*money', r'prize', r'cash', r'million', r'thousand']
    if any(re.search(pattern, text) for pattern in money_patterns):
        factors.append("monetary claim")
        confidence += 0.3
    
    # Check for call to action
    action_words = ['click here', 'call now', 'visit', 'claim', 'download', 'subscribe']
    if any(word in text for word in action_words):
        factors.append("call to action")
        confidence += 0.2
    
    # Check for excessive punctuation
    if re.search(r'[!]{2,}', subject + body):
        factors.append("excessive punctuation")
        confidence += 0.2
    
    # Check for suspicious phrases
    suspicious_phrases = ['no purchase necessary', 'free', 'guarantee', 'risk free', 'special offer']
    if any(phrase in text for phrase in suspicious_phrases):
        factors.append("suspicious phrases")
        confidence += 0.15
    
    # Check for all caps words
    if re.search(r'\b[A-Z]{3,}\b', subject + body):
        factors.append("excessive capitalization")
        confidence += 0.1
    
    # Cap confidence at 1.0
    confidence = min(confidence, 1.0)
    
    # Determine if spam (threshold of 0.4)
    is_spam = confidence >= 0.4
    
    return is_spam, confidence, factors

def main():
    input_data = sys.stdin.read().strip()
    data = json.loads(input_data)
    
    subject = data["subject"]
    body = data["body"]
    
    is_spam, confidence, factors = analyze_spam(subject, body)
    
    result = {
        "is_spam": is_spam,
        "confidence": confidence,
        "factors": factors
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()