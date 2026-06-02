secret = input().strip()
guess = input().strip()

# Count black pegs (exact matches)
black = 0
secret_remaining = []
guess_remaining = []

for i in range(4):
    if secret[i] == guess[i]:
        black += 1
    else:
        secret_remaining.append(secret[i])
        guess_remaining.append(guess[i])

# Count white pegs (color matches in wrong position)
white = 0
secret_counts = {}
guess_counts = {}

# Count occurrences of each digit in remaining positions
for digit in secret_remaining:
    secret_counts[digit] = secret_counts.get(digit, 0) + 1

for digit in guess_remaining:
    guess_counts[digit] = guess_counts.get(digit, 0) + 1

# White pegs are minimum of counts for each digit
for digit in guess_counts:
    if digit in secret_counts:
        white += min(secret_counts[digit], guess_counts[digit])

print(black, white)