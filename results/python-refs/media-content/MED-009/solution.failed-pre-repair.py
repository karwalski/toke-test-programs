import sys
import re

def count_syllables(word):
    # Remove punctuation and convert to lowercase
    word = re.sub(r'[^a-zA-Z]', '', word).lower()
    if not word:
        return 0
    
    # Count vowel groups
    vowels = 'aeiouy'
    syllable_count = 0
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            syllable_count += 1
        prev_was_vowel = is_vowel
    
    # Handle silent 'e' at the end
    if word.endswith('e') and syllable_count > 1:
        syllable_count -= 1
    
    # Every word has at least one syllable
    return max(1, syllable_count)

def is_complex_word(word):
    return count_syllables(word) >= 3

def gunning_fog_index(text):
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 0.0
    
    # Count words and complex words
    total_words = 0
    complex_words = 0
    
    for sentence in sentences:
        words = re.findall(r'\b[a-zA-Z]+\b', sentence)
        total_words += len(words)
        
        for word in words:
            if is_complex_word(word):
                complex_words += 1
    
    if total_words == 0:
        return 0.0
    
    # Gunning Fog Index formula
    avg_sentence_length = total_words / len(sentences)
    percent_complex = (complex_words / total_words) * 100
    
    fog_index = 0.4 * (avg_sentence_length + percent_complex)
    
    return fog_index

# Read input from stdin
text = sys.stdin.read().strip()

# Calculate Gunning Fog Index
fog = gunning_fog_index(text)

# Output result
print(f"fog: {fog:.1f}")