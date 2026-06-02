import sys

# Standard Scrabble letter values
letter_values = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8,
    'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1,
    'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
}

lines = sys.stdin.read().strip().split('\n')
word = lines[0].upper()

# Initialize multipliers
letter_multipliers = [1] * len(word)
word_multiplier = 1

# Process multiplier squares
for i in range(1, len(lines)):
    if lines[i].strip():
        parts = lines[i].strip().split()
        pos = int(parts[0])
        mult_type = parts[1]
        
        if mult_type == 'DL':
            letter_multipliers[pos] = 2
        elif mult_type == 'TL':
            letter_multipliers[pos] = 3
        elif mult_type == 'DW':
            word_multiplier *= 2
        elif mult_type == 'TW':
            word_multiplier *= 3

# Calculate score
total_score = 0
for i, letter in enumerate(word):
    letter_score = letter_values[letter] * letter_multipliers[i]
    total_score += letter_score

total_score *= word_multiplier

print(total_score)