import sys
import math

lines = sys.stdin.read().strip().split('\n')

# Parse WPM from first line
try:
    wpm = int(lines[0])
    text_lines = lines[1:]
except (ValueError, IndexError):
    wpm = 200
    text_lines = lines

# Count words in remaining text
word_count = 0
for line in text_lines:
    words = line.split()
    word_count += len(words)

# Calculate reading time and round up
reading_time_minutes = math.ceil(word_count / wpm) if word_count > 0 else 0

print(f"reading_time: {reading_time_minutes} min")
print(f"word_count: {word_count}")