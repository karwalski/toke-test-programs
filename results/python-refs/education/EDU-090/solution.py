import sys
import re
import math

def count_syllables(word):
    word = word.lower().strip()
    if not word:
        return 0
    
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
    
    # Every word has at least 1 syllable
    return max(1, syllable_count)

def calculate_grade_level(text):
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 1
    
    # Count words and syllables
    total_words = 0
    total_syllables = 0
    
    for sentence in sentences:
        words = re.findall(r'\b[a-zA-Z]+\b', sentence)
        total_words += len(words)
        for word in words:
            total_syllables += count_syllables(word)
    
    if total_words == 0:
        return 1
    
    # Flesch-Kincaid Grade Level formula
    avg_sentence_length = total_words / len(sentences)
    avg_syllables_per_word = total_syllables / total_words
    
    grade_level = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
    
    return max(1, round(grade_level))

# Read input
target_grade = int(input().strip())
text_lines = []
try:
    while True:
        line = input()
        text_lines.append(line)
except EOFError:
    pass

text = '\n'.join(text_lines)

# Calculate actual grade level
actual_grade = calculate_grade_level(text)

# Output result
if actual_grade == target_grade:
    print("APPROPRIATE")
elif actual_grade < target_grade:
    print(f"TOO EASY (grade {actual_grade})")
else:
    print(f"TOO HARD (grade {actual_grade})")