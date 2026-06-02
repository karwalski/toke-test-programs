import json
import sys
import re
from difflib import SequenceMatcher

def preprocess_text(text):
    """Normalize text for comparison"""
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove punctuation except letters, numbers, and spaces
    text = re.sub(r'[^\w\s]', '', text)
    return text

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts"""
    # Preprocess both texts
    text1_clean = preprocess_text(text1)
    text2_clean = preprocess_text(text2)
    
    # Use SequenceMatcher to get similarity ratio
    similarity = SequenceMatcher(None, text1_clean, text2_clean).ratio()
    
    return similarity

def find_duplicate(new_item, existing_items, threshold=0.8):
    """Find if new_item is a duplicate of any existing item"""
    best_similarity = 0
    best_match_id = None
    
    for item in existing_items:
        similarity = calculate_similarity(new_item, item['text'])
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_id = item['id']
    
    is_duplicate = best_similarity >= threshold
    duplicate_of = best_match_id if is_duplicate else None
    
    return is_duplicate, duplicate_of, round(best_similarity, 1)

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())
    
    new_item = input_data['new_item']
    existing_items = input_data['existing_items']
    
    # Find duplicates
    is_duplicate, duplicate_of, similarity = find_duplicate(new_item, existing_items)
    
    # Create output
    result = {
        "is_duplicate": is_duplicate,
        "duplicate_of": duplicate_of,
        "similarity": similarity
    }
    
    # Output JSON with no extra whitespace
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()