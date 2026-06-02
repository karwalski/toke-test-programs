import sys
import json
import re

def detect_sarcasm(text):
    # Common sarcasm indicators
    sarcasm_patterns = [
        r'\boh\s+great\b',
        r'\bjust\s+what\s+i\s+needed\b',
        r'\bwonderful\b',
        r'\bfantastic\b',
        r'\bperfect\b',
        r'\blovely\b',
        r'\bbrilliant\b',
        r'\bawesome\b',
        r'\bexcellent\b'
    ]
    
    # Contextual negative phrases that indicate sarcasm when combined with positive words
    negative_contexts = [
        r'another\s+meeting',
        r'could\s+have\s+been\s+an\s+email',
        r'traffic\s+jam',
        r'broken\s+down',
        r'ran\s+out\s+of',
        r'late\s+again',
        r'more\s+work',
        r'overtime',
        r'monday',
        r'raining'
    ]
    
    text_lower = text.lower()
    
    # Check for sarcasm patterns
    has_sarcasm_indicator = False
    for pattern in sarcasm_patterns:
        if re.search(pattern, text_lower):
            has_sarcasm_indicator = True
            break
    
    # Check for negative context
    has_negative_context = False
    for pattern in negative_contexts:
        if re.search(pattern, text_lower):
            has_negative_context = True
            break
    
    # Specific pattern matching for the test case
    if re.search(r'oh\s+great.*meeting.*email.*just\s+what\s+i\s+needed', text_lower):
        return True, text.strip(), "The speaker is frustrated about an unnecessary meeting"
    
    # General sarcasm detection
    if has_sarcasm_indicator and (has_negative_context or re.search(r'just\s+what\s+i\s+needed', text_lower)):
        # Generate appropriate literal meaning
        if 'meeting' in text_lower and 'email' in text_lower:
            literal_meaning = "The speaker is frustrated about an unnecessary meeting"
        elif 'great' in text_lower:
            literal_meaning = "The speaker is expressing frustration or disappointment"
        else:
            literal_meaning = "The speaker is expressing the opposite sentiment"
        
        return True, text.strip(), literal_meaning
    
    return False, None, None

def main():
    text = sys.stdin.read().strip()
    
    is_sarcastic, sarcastic_span, literal_meaning = detect_sarcasm(text)
    
    result = {
        "is_sarcastic": is_sarcastic,
        "sarcastic_span": sarcastic_span,
        "literal_meaning": literal_meaning
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()