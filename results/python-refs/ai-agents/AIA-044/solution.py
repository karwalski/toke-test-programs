import sys
import json
import re
import string

def count_syllables(word):
    """Simple syllable counting heuristic"""
    word = word.lower().strip(string.punctuation)
    if not word:
        return 0
    
    vowels = "aeiouy"
    syllable_count = 0
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            syllable_count += 1
        prev_was_vowel = is_vowel
    
    # Handle silent e
    if word.endswith('e') and syllable_count > 1:
        syllable_count -= 1
    
    return max(1, syllable_count)

def is_technical_term(word):
    """Check if a word is likely a technical term"""
    word = word.lower().strip(string.punctuation)
    
    # Simple heuristics for technical terms
    technical_indicators = [
        len(word) > 8,  # Long words are often technical
        word.endswith(('tion', 'sion', 'ment', 'ness', 'ity', 'ism', 'ology', 'graphy')),
        word.startswith(('pre', 'post', 'anti', 'pro', 'meta', 'micro', 'macro')),
        any(char.isdigit() for char in word),  # Contains numbers
    ]
    
    return any(technical_indicators)

def analyze_text(text):
    # Split into sentences
    sentences = re.split(r'[.!?]+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {"level": "elementary", "metrics": {"avg_sentence_length": 0, "vocabulary_complexity": "simple", "technical_terms_count": 0}}
    
    # Calculate average sentence length
    total_words = 0
    all_words = []
    technical_count = 0
    
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence)
        total_words += len(words)
        all_words.extend(words)
        
        # Count technical terms
        for word in words:
            if is_technical_term(word):
                technical_count += 1
    
    avg_sentence_length = round(total_words / len(sentences)) if sentences else 0
    
    # Calculate vocabulary complexity
    if not all_words:
        vocab_complexity = "simple"
    else:
        # Calculate average syllables per word
        total_syllables = sum(count_syllables(word) for word in all_words)
        avg_syllables = total_syllables / len(all_words)
        
        # Determine vocabulary complexity
        if avg_syllables <= 1.3:
            vocab_complexity = "simple"
        elif avg_syllables <= 1.7:
            vocab_complexity = "moderate"
        else:
            vocab_complexity = "complex"
    
    # Determine overall level
    if avg_sentence_length <= 8 and vocab_complexity == "simple" and technical_count == 0:
        level = "elementary"
    elif avg_sentence_length <= 15 and vocab_complexity in ["simple", "moderate"] and technical_count <= 2:
        level = "intermediate"
    elif avg_sentence_length <= 20 and technical_count <= 5:
        level = "advanced"
    else:
        level = "expert"
    
    return {
        "level": level,
        "metrics": {
            "avg_sentence_length": avg_sentence_length,
            "vocabulary_complexity": vocab_complexity,
            "technical_terms_count": technical_count
        }
    }

# Read input from stdin
text = sys.stdin.read().strip()

# Analyze the text
result = analyze_text(text)

# Output JSON
print(json.dumps(result, separators=(',', ':')))