import json
import sys
from difflib import SequenceMatcher

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts using SequenceMatcher"""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def classify_intent(user_text, intents):
    """Classify user input into one of the provided intent categories"""
    best_intent = None
    best_score = 0.0
    
    user_text_lower = user_text.lower()
    
    for intent in intents:
        intent_score = 0.0
        
        # Check similarity with description
        desc_similarity = calculate_similarity(user_text_lower, intent['description'].lower())
        intent_score = max(intent_score, desc_similarity)
        
        # Check similarity with examples
        for example in intent.get('examples', []):
            example_similarity = calculate_similarity(user_text_lower, example.lower())
            intent_score = max(intent_score, example_similarity)
        
        # Check for keyword matches
        intent_words = set(intent['label'].lower().split())
        user_words = set(user_text_lower.split())
        
        # Look for exact matches or partial matches in the text
        for word in intent_words:
            if word in user_text_lower:
                intent_score = max(intent_score, 0.8)
        
        # Special handling for common patterns
        if intent['label'].lower() == 'cancel':
            cancel_keywords = ['cancel', 'stop', 'end', 'terminate', 'quit', 'unsubscribe']
            for keyword in cancel_keywords:
                if keyword in user_text_lower:
                    intent_score = max(intent_score, 0.95)
        
        if intent_score > best_score:
            best_score = intent_score
            best_intent = intent['label']
    
    # Ensure minimum confidence for matches
    if best_score < 0.3:
        best_score = 0.3
    
    return best_intent, best_score

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    user_text = input_data['text']
    intents = input_data['intents']
    
    # Classify the intent
    intent_label, confidence = classify_intent(user_text, intents)
    
    # Create output
    result = {
        "intent": intent_label,
        "confidence": confidence
    }
    
    # Output JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()