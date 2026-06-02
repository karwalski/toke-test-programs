import sys

# Read the secret number
secret = int(input().strip())

# Process each guess
for line in sys.stdin:
    guess = int(line.strip())
    
    if guess < secret:
        print("Too low")
    elif guess > secret:
        print("Too high")
    else:
        print("Correct!")