import sys
import random

# Read sample rate
sample_rate = float(input().strip())

# Read seed
seed = int(input().strip())

# Set the random seed for deterministic sampling
random.seed(seed)

# Read all log lines
log_lines = []
try:
    while True:
        line = input()
        log_lines.append(line)
except EOFError:
    pass

# Sample the log lines
for line in log_lines:
    if random.random() < sample_rate:
        print(line)