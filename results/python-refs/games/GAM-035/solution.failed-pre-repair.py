import random

def spin_reel():
    # Common slot machine symbols with different probabilities
    symbols = ['7', 'BAR', 'CHERRY', 'LEMON', 'ORANGE', 'BELL']
    return random.choice(symbols)

def calculate_payout(reel1, reel2, reel3, bet):
    # Check for winning combinations
    if reel1 == reel2 == reel3:
        # Three of a kind
        if reel1 == '7':
            return bet * 100  # Jackpot
        elif reel1 == 'BAR':
            return bet * 50
        elif reel1 == 'CHERRY':
            return bet * 25
        elif reel1 == 'BELL':
            return bet * 20
        else:
            return bet * 10
    elif reel1 == reel2 or reel2 == reel3 or reel1 == reel3:
        # Two of a kind
        if 'CHERRY' in [reel1, reel2, reel3]:
            return bet * 2
        else:
            return bet * 1
    elif 'CHERRY' in [reel1, reel2, reel3]:
        # At least one cherry
        cherry_count = [reel1, reel2, reel3].count('CHERRY')
        if cherry_count >= 2:
            return bet * 3
        else:
            return bet * 1
    else:
        return 0

# Read input
line = input().strip()
spins, bet, seed = map(int, line.split())

# Set random seed
random.seed(seed)

total_payout = 0

# Simulate spins
for _ in range(spins):
    reel1 = spin_reel()
    reel2 = spin_reel() 
    reel3 = spin_reel()
    
    payout = calculate_payout(reel1, reel2, reel3, bet)
    total_payout += payout

# Calculate net gain/loss
total_bet = spins * bet
net = total_payout - total_bet

# Output results
print(f"Total payout: {total_payout}")
print(f"Net: {net}")