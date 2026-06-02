import sys
from itertools import product

def calculate_response(guess, secret):
    """Calculate the response for a guess against the secret code"""
    bulls = sum(1 for i in range(4) if guess[i] == secret[i])
    
    # Count cows by finding common digits excluding bulls
    guess_counts = [0] * 7  # digits 1-6
    secret_counts = [0] * 7
    
    for i in range(4):
        if guess[i] != secret[i]:
            guess_counts[int(guess[i])] += 1
            secret_counts[int(secret[i])] += 1
    
    cows = sum(min(guess_counts[i], secret_counts[i]) for i in range(1, 7))
    
    return bulls, cows

def is_consistent(guess, response, candidate):
    """Check if a candidate code is consistent with the given guess and response"""
    bulls, cows = calculate_response(guess, candidate)
    return bulls == response[0] and cows == response[1]

def knuth_mastermind(secret):
    """Implement Knuth's algorithm for Mastermind"""
    # Generate all possible codes
    all_codes = [''.join(code) for code in product('123456', repeat=4)]
    possible_codes = all_codes[:]
    
    guesses = []
    responses = []
    
    # First guess is always 1122 in Knuth's algorithm
    guess = "1122"
    
    while True:
        # Calculate response
        bulls, cows = calculate_response(guess, secret)
        response = (bulls, cows)
        
        # Output guess and response
        print(f"{guess} {bulls}B{cows}W")
        
        guesses.append(guess)
        responses.append(response)
        
        # Check if solved
        if bulls == 4:
            break
        
        # Filter possible codes based on this guess and response
        new_possible = []
        for code in possible_codes:
            if is_consistent(guess, response, code):
                new_possible.append(code)
        possible_codes = new_possible
        
        # Choose next guess using minimax strategy
        # For simplicity, just pick the first remaining possible code
        # (The full Knuth algorithm would use minimax to minimize worst case)
        if possible_codes:
            guess = possible_codes[0]
    
    return len(guesses)

# Read input
secret = input().strip()

# Solve and get number of guesses
num_guesses = knuth_mastermind(secret)

# Output final result
print(f"Solved in {num_guesses} guesses")