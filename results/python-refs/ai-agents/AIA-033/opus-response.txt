import json
import sys
import re

def analyze_spam(subject, body):
    factors = []
    text = (subject + " " + body).lower()
    
    urgency_words = ['urgent', 'hurry', 'limited time', 'act now', 'expires']
    if any(word in text for word in urgency_words):
        factors.append("urgency language")
    
    money_patterns = [r'\$[\d,]+', r'won.*money', r'prize', r'million']
    if any(re.search(pattern, text) for pattern in money_patterns):
        factors.append("monetary claim")
    
    action_words = ['click here', 'call now', 'claim your', 'download now', 'subscribe now']
    if any(word in text for word in action_words):
        factors.append("call to action")
    
    if re.search(r'[!]{2,}', subject + body):
        factors.append("excessive punctuation")
    
    if factors:
        is_spam = True
        confidence = 0.95
    else:
        is_spam = False
        confidence = 0.98
    
    return is_spam, confidence, factors

def main():
    data = json.loads(sys.stdin.read().strip())
    is_spam, confidence, factors = analyze_spam(data["subject"], data["body"])
    result = {"is_spam": is_spam, "confidence": confidence, "factors": factors}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()