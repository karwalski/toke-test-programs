word = input().strip()
guessed_letters = input().strip().split()

# Convert to uppercase for case-insensitive comparison
word = word.upper()
guessed_letters = [letter.upper() for letter in guessed_letters]

# Create masked word
masked_word = ""
for letter in word:
    if letter in guessed_letters:
        masked_word += letter
    else:
        masked_word += "_"

# Count wrong guesses
wrong_guesses = 0
for letter in guessed_letters:
    if letter not in word:
        wrong_guesses += 1

# Calculate remaining lives (start with 6, lose 1 per wrong guess)
remaining_lives = 6 - wrong_guesses

print(masked_word)
print(remaining_lives)