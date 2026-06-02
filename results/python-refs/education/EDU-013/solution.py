import sys

# Read input
target_text = input().strip()
typed_text = input().strip()
elapsed_seconds = int(input().strip())

# Calculate errors by comparing character by character
errors = 0
min_length = min(len(target_text), len(typed_text))

# Count character mismatches
for i in range(min_length):
    if target_text[i] != typed_text[i]:
        errors += 1

# Add errors for length differences
errors += abs(len(target_text) - len(typed_text))

# Calculate accuracy
if len(target_text) == 0:
    accuracy = 100
else:
    accuracy = max(0, 100 - (errors * 100 // len(target_text)))

# Calculate WPM (words per minute)
# Standard: 5 characters = 1 word
chars_typed = len(typed_text)
words_typed = chars_typed / 5
minutes = elapsed_seconds / 60
wpm = int(words_typed / minutes) if minutes > 0 else 0

# Output results
print(f"wpm: {wpm}")
print(f"accuracy: {accuracy}%")
print(f"errors: {errors}")