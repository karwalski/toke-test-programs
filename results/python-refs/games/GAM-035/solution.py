<think>
Let me try the logic and see if it matches. I need to test mentally or just try the most likely interpretation. Let me write clean code.
</think>

import random
line = input().split()
spins, bet, seed = int(line[0]), int(line[1]), int(line[2])
random.seed(seed)
symbols = ['cherry','lemon','orange','plum','bell','bar','sevens']
total = 0
for _ in range(spins):
    r = [random.choice(symbols) for _ in range(3)]
    if r[0]==r[1]==r[2]:
        total += 10*bet
    elif r[0]==r[1] or r[1]==r[2] or r[0]==r[2]:
        total += bet
print(f"Total payout: {total}")
print(f"Net: {total - spins*bet}")