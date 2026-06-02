import sys

# Read input
lines = [line.strip() for line in sys.stdin.readlines()]
word_list = lines[0].split()
secret_word = lines[1]

# Create rank mapping
word_to_rank = {word: i + 1 for i, word in enumerate(word_list)}
secret_rank = word_to_rank[secret_word]

# Process guesses
previous_distance = None

for i in range(2, len(lines)):
    guess = lines[i]
    guess_rank = word_to_rank[guess]
    distance = abs(guess_rank - secret_rank)
    
    if guess == secret_word:
        print(f"Guess: {guess} - Rank {guess_rank} - Correct!")
        break
    else:
        if previous_distance is None:
            comparison = "colder"
        elif distance < previous_distance:
            comparison = "warmer"
        else:
            comparison = "colder"
        
        print(f"Guess: {guess} - Rank {guess_rank} - Distance {distance} {comparison}")
        previous_distance = distance