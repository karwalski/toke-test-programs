import json
import sys
import re

def detect_errors(source_text, translated_text, source_lang, target_lang):
    """Detect translation errors without reference translation"""
    errors = []
    
    # Basic punctuation check
    source_punct = re.findall(r'[.!?;:,]', source_text)
    target_punct = re.findall(r'[.!?;:,]', translated_text)
    
    # Check for missing punctuation
    if len(source_punct) != len(target_punct):
        # Find missing punctuation
        for i, punct in enumerate(source_punct):
            if i >= len(target_punct) or target_punct[i] != punct:
                errors.append({
                    "type": "punctuation",
                    "span": [len(translated_text)-1, len(translated_text)],
                    "suggestion": f"Missing punctuation: {punct}"
                })
                break
    
    # Check for untranslated words (words that appear identical in both languages)
    source_words = re.findall(r'\b\w+\b', source_text.lower())
    target_words = re.findall(r'\b\w+\b', translated_text.lower())
    
    # Simple check for completely untranslated content
    if source_text.strip() == translated_text.strip():
        errors.append({
            "type": "untranslated",
            "span": [0, len(translated_text)],
            "suggestion": "Text appears to be untranslated"
        })
    
    # Check for obvious formatting issues
    if source_text.isupper() and not translated_text.isupper():
        errors.append({
            "type": "formatting",
            "span": [0, len(translated_text)],
            "suggestion": "Case formatting inconsistency"
        })
    
    # Check for excessive length differences (potential over/under translation)
    length_ratio = len(translated_text) / len(source_text) if len(source_text) > 0 else 1
    if length_ratio > 3 or length_ratio < 0.3:
        errors.append({
            "type": "length",
            "span": [0, len(translated_text)],
            "suggestion": "Translation length seems inconsistent with source"
        })
    
    return errors

def calculate_quality_score(source_text, translated_text, errors):
    """Calculate quality score based on detected errors"""
    base_score = 1.0
    
    # Deduct points for each error type
    for error in errors:
        if error["type"] == "punctuation":
            base_score -= 0.05
        elif error["type"] == "untranslated":
            base_score -= 0.5
        elif error["type"] == "formatting":
            base_score -= 0.1
        elif error["type"] == "length":
            base_score -= 0.3
        else:
            base_score -= 0.1
    
    # Ensure score is between 0 and 1
    return max(0.0, min(1.0, base_score))

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    source_text = input_data["source_text"]
    translated_text = input_data["translated_text"]
    source_lang = input_data["source_lang"]
    target_lang = input_data["target_lang"]
    
    # Detect errors
    errors = detect_errors(source_text, translated_text, source_lang, target_lang)
    
    # Calculate quality score
    quality_score = calculate_quality_score(source_text, translated_text, errors)
    
    # Create output
    output = {
        "quality_score": quality_score,
        "errors": errors
    }
    
    # Output JSON
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()