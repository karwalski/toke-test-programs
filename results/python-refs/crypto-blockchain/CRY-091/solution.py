block_height = int(input())

# Initial reward is 50 BTC
reward = 50.0

# Calculate number of halvings (every 210,000 blocks)
halvings = block_height // 210000

# Apply halvings
for _ in range(halvings):
    reward /= 2

# Format output to remove unnecessary decimal places
if reward == int(reward):
    print(int(reward))
else:
    print(reward)