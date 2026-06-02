import sys

def evaluate_guess(secret, guess):
    bulls = 0
    cows = 0
    
    # Convert to strings to work with individual digits
    secret_str = str(secret)
    guess_str = str(guess)
    
    # Count bulls (correct digit in correct position)
    for i in range(4):
        if secret_str[i] == guess_str[i]:
            bulls += 1
    
    # Count cows (correct digit in wrong position)
    for digit in guess_str:
        if digit in secret_str:
            cows += 1
    
    # Subtract bulls from cows since bulls were counted in cows
    cows -= bulls
    
    return bulls, cows

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

secret = int(lines[0])
guesses = [int(line) for line in lines[1:]]

# Process each guess
for guess in guesses:
    bulls, cows = evaluate_guess(secret, guess)
    print(f"{bulls}A{cows}B")