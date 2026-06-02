import json
import sys

# Read the dictionary line
dict_line = input().strip()
dictionary = json.loads(dict_line)

# Process translation attempts
correct = 0
total = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    word, attempted_translation = line.split('=', 1)
    correct_translation = dictionary[word]
    
    total += 1
    if attempted_translation == correct_translation:
        print(f"{word}: Correct")
        correct += 1
    else:
        print(f"{word}: Incorrect ({correct_translation})")

# Calculate and print score
percentage = int(correct / total * 100)
print(f"Score: {correct}/{total} ({percentage}%)")