import random

def analytical_probability(n):
    if n == 1:
        return 0.0
    
    # Probability that all people have different birthdays
    prob_all_different = 1.0
    for i in range(n):
        prob_all_different *= (365 - i) / 365
    
    # Probability that at least two share a birthday
    return 1.0 - prob_all_different

def simulate_birthday_probability(n, simulations):
    if n == 1:
        return 0.0
    
    matches = 0
    for _ in range(simulations):
        birthdays = [random.randint(1, 365) for _ in range(n)]
        if len(set(birthdays)) < len(birthdays):
            matches += 1
    
    return matches / simulations

# Read input
max_group_size = int(input())
simulations = int(input())

# Process each group size
for n in range(1, max_group_size + 1):
    analytical = analytical_probability(n)
    simulated = simulate_birthday_probability(n, simulations)
    
    print(f"{n}: analytical={analytical:.4f} simulated={simulated:.4f}")