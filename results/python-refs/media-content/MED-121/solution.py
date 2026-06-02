import sys
import re
import math

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
    if word.endswith('e'):
        syllable_count -= 1
    
    # Every word has at least one syllable
    return max(1, syllable_count)

def flesch_kincaid_grade(text):
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Split into words
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    
    if not sentences or not words:
        return 0
    
    # Count syllables
    total_syllables = sum(count_syllables(word) for word in words)
    
    # Calculate Flesch-Kincaid Grade Level
    grade = (0.39 * len(words) / len(sentences)) + (11.8 * total_syllables / len(words)) - 15.59
    
    return round(grade)

def get_level_label(grade):
    if grade <= 6:
        return "Elementary"
    elif grade <= 8:
        return "Middle School"
    elif grade <= 12:
        return "High School"
    else:
        return "College"

# Read input
text = sys.stdin.read().strip()

# Calculate grade
grade = flesch_kincaid_grade(text)
label = get_level_label(grade)

# Output
print(f"grade: {grade}")
print(f"level: {label}")