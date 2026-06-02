import sys
import json
import re

def classify_sentiment(text):
    # Define sentiment word lists
    positive_words = [
        'love', 'excellent', 'amazing', 'fantastic', 'wonderful', 'great', 'awesome',
        'brilliant', 'perfect', 'outstanding', 'superb', 'magnificent', 'marvelous',
        'incredible', 'fabulous', 'terrific', 'good', 'nice', 'beautiful', 'best',
        'better', 'happy', 'pleased', 'satisfied', 'delighted', 'thrilled', 'excited',
        'absolutely', 'definitely', 'certainly', 'highly', 'recommend', 'impressed'
    ]
    
    negative_words = [
        'hate', 'terrible', 'awful', 'horrible', 'disgusting', 'disappointing',
        'worst', 'bad', 'poor', 'useless', 'broken', 'defective', 'waste',
        'money', 'regret', 'never', 'avoid', 'pathetic', 'ridiculous', 'annoying',
        'frustrated', 'angry', 'upset', 'dissatisfied', 'unhappy', 'worse'
    ]
    
    # Positive and negative phrase patterns
    positive_phrases = [
        r'absolutely love', r'best purchase', r'highly recommend', r'love it',
        r'amazing quality', r'perfect for', r'excellent value', r'great product',
        r'very happy', r'extremely pleased', r'fantastic experience'
    ]
    
    negative_phrases = [
        r'waste of money', r'very disappointed', r'terrible quality', r'worst purchase',
        r'complete garbage', r'absolutely hate', r'never again', r'avoid at all costs',
        r'extremely poor', r'totally useless'
    ]
    
    text_lower = text.lower()
    
    # Find key phrases
    key_phrases = []
    
    # Check for positive phrases
    for phrase_pattern in positive_phrases:
        matches = re.findall(phrase_pattern, text_lower)
        key_phrases.extend(matches)
    
    # Check for negative phrases
    for phrase_pattern in negative_phrases:
        matches = re.findall(phrase_pattern, text_lower)
        key_phrases.extend(matches)
    
    # Count positive and negative words
    words = re.findall(r'\b\w+\b', text_lower)
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    
    # Calculate sentiment and confidence
    total_sentiment_words = positive_count + negative_count
    
    if total_sentiment_words == 0:
        sentiment = "neutral"
        confidence = 0.5
    elif positive_count > negative_count:
        sentiment = "positive"
        # Calculate confidence based on ratio and presence of strong indicators
        ratio = positive_count / total_sentiment_words
        confidence = min(0.95, 0.6 + (ratio * 0.35))
        
        # Boost confidence for strong positive indicators
        if any(phrase in text_lower for phrase in ['absolutely love', 'best purchase']):
            confidence = 0.95
            
    elif negative_count > positive_count:
        sentiment = "negative"
        ratio = negative_count / total_sentiment_words
        confidence = min(0.95, 0.6 + (ratio * 0.35))
        
        # Boost confidence for strong negative indicators
        if any(phrase in text_lower for phrase in ['waste of money', 'absolutely hate']):
            confidence = 0.95
    else:
        sentiment = "neutral"
        confidence = 0.6
    
    return sentiment, confidence, key_phrases

def main():
    # Read input from stdin
    text = sys.stdin.read().strip()
    
    # Classify sentiment
    sentiment, confidence, key_phrases = classify_sentiment(text)
    
    # Create output JSON
    result = {
        "sentiment": sentiment,
        "confidence": confidence,
        "key_phrases": key_phrases
    }
    
    # Output JSON without spaces after separators to match expected format
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()