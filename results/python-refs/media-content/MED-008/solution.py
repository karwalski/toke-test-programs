import sys
import re

def count_syllables(word):
    word = word.lower()
    # Remove non-alphabetic characters
    word = re.sub(r'[^a-z]', '', word)
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
    
    # Handle silent e
    if word.endswith('e') and syllable_count > 1:
        syllable_count -= 1
    
    # Every word has at least one syllable
    return max(1, syllable_count)

def flesch_kincaid_score(text):
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Split into words
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    
    if not sentences or not words:
        return 0.0
    
    # Count syllables
    total_syllables = sum(count_syllables(word) for word in words)
    
    # Calculate FK Reading Ease score
    score = 206.835 - (1.015 * len(words) / len(sentences)) - (84.6 * total_syllables / len(words))
    
    return score

# Read input
text = sys.stdin.read().strip()

# Calculate and output score
score = flesch_kincaid_score(text)
print(f"score: {score:.1f}")