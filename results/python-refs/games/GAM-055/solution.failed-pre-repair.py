import sys
import random

def get_color(number):
    if number == 0:
        return "Green"
    # Standard roulette: Red numbers are 1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36
    red_numbers = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    if number in red_numbers:
        return "Red"
    else:
        return "Black"

def calculate_winnings(bet_type, bet_amount, spin_result):
    if bet_type == "red":
        if get_color(spin_result) == "Red":
            return bet_amount  # 1:1 payout
        else:
            return -bet_amount
    elif bet_type == "black":
        if get_color(spin_result) == "Black":
            return bet_amount  # 1:1 payout
        else:
            return -bet_amount
    elif bet_type.startswith("number"):
        bet_number = int(bet_type[6:])  # Extract number after "number"
        if spin_result == bet_number:
            return bet_amount * 35  # 35:1 payout
        else:
            return -bet_amount
    return -bet_amount

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

starting_balance = int(lines[0])
seed = int(lines[1])
bets = []

for i in range(2, len(lines)):
    if lines[i]:
        parts = lines[i].split()
        bet_type = parts[0]
        bet_amount = int(parts[1])
        bets.append((bet_type, bet_amount))

# Set random seed
random.seed(seed)

# Simulate spins
balance = starting_balance
for i, (bet_type, bet_amount) in enumerate(bets, 1):
    # Generate spin result (0-36 for European roulette)
    spin_result = random.randint(0, 36)
    color = get_color(spin_result)
    
    # Calculate winnings
    winnings = calculate_winnings(bet_type, bet_amount, spin_result)
    balance += winnings
    
    # Format output
    if winnings > 0:
        print(f"Spin {i}: {spin_result} {color} - Win ${winnings} - Balance: ${balance}")
    else:
        print(f"Spin {i}: {spin_result} {color} - Lose ${-winnings} - Balance: ${balance}")