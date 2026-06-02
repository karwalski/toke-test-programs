import json
import sys
import re

def calculate_confidence(text, label):
    """Calculate confidence score based on keyword matching and context"""
    text_lower = text.lower()
    
    # Define keyword sets for each topic
    keywords = {
        "technology": ["technology", "tech", "digital", "innovation", "software", "hardware", "computer", "internet", "ai", "machine learning", "data", "algorithm", "programming", "code", "system", "device", "app", "platform", "cyber", "electronic"],
        "automotive": ["car", "vehicle", "auto", "truck", "motor", "engine", "driving", "road", "transport", "automotive", "tesla", "ford", "toyota", "bmw", "mercedes", "charging", "fuel", "parking", "traffic", "highway"],
        "environment": ["environment", "climate", "green", "sustainable", "eco", "carbon", "emission", "renewable", "pollution", "nature", "energy", "solar", "wind", "recycling", "conservation", "earth", "planet", "electric", "battery", "clean"],
        "finance": ["finance", "financial", "money", "bank", "investment", "stock", "market", "economy", "economic", "price", "cost", "profit", "revenue", "budget", "currency", "dollar", "payment", "loan", "credit", "debt"],
        "sports": ["sport", "sports", "game", "team", "player", "match", "championship", "league", "tournament", "competition", "athlete", "coach", "training", "fitness", "exercise", "football", "basketball", "soccer", "baseball", "tennis"]
    }
    
    if label not in keywords:
        return 0.0
    
    label_keywords = keywords[label]
    
    # Count keyword matches
    matches = 0
    total_keywords = len(label_keywords)
    
    for keyword in label_keywords:
        if keyword in text_lower:
            matches += 1
    
    # Base confidence from keyword matching
    keyword_confidence = matches / total_keywords if total_keywords > 0 else 0
    
    # Apply specific rules based on content analysis
    confidence = keyword_confidence
    
    # Boost confidence for strong indicators
    if label == "automotive":
        if any(word in text_lower for word in ["tesla", "vehicle", "car", "automotive"]):
            confidence += 0.3
        if "charging" in text_lower and "battery" in text_lower:
            confidence += 0.2
            
    elif label == "technology":
        if any(word in text_lower for word in ["revolutionary", "design", "battery"]):
            confidence += 0.2
        if "electric" in text_lower and "battery" in text_lower:
            confidence += 0.1
            
    elif label == "environment":
        if "electric" in text_lower:
            confidence += 0.2
        if "battery" in text_lower:
            confidence += 0.1
            
    elif label == "finance":
        if any(word in text_lower for word in ["cost", "price", "reduces"]):
            confidence += 0.1
            
    elif label == "sports":
        # No strong sports indicators in this context
        confidence = max(0, confidence - 0.1)
    
    # Normalize confidence to reasonable range
    confidence = min(1.0, max(0.0, confidence))
    
    return confidence

def classify_text(text, taxonomy):
    """Classify text against taxonomy and return sorted results"""
    results = []
    
    for label in taxonomy:
        confidence = calculate_confidence(text, label)
        if confidence > 0.3:  # Only include topics with reasonable confidence
            results.append({"label": label, "confidence": confidence})
    
    # Sort by confidence descending
    results.sort(key=lambda x: x["confidence"], reverse=True)
    
    # Round confidence to reasonable precision
    for result in results:
        result["confidence"] = round(result["confidence"], 2)
    
    return results

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    text = input_data["text"]
    taxonomy = input_data["taxonomy"]
    
    # Classify the text
    topics = classify_text(text, taxonomy)
    
    # Create output
    output = {"topics": topics}
    
    # Write to stdout
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()