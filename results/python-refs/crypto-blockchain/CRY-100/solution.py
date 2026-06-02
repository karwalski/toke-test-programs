import json
import sys

# Read input
line1 = input().strip()
line2 = input().strip()

chain_a = json.loads(line1)
chain_b = json.loads(line2)

# Find fork point (last common block)
fork_point = None
min_len = min(len(chain_a), len(chain_b))

for i in range(min_len):
    if chain_a[i] == chain_b[i]:
        fork_point = chain_a[i]
    else:
        break

# Count blocks after fork
fork_index = -1
if fork_point:
    # Find the index of the fork point
    for i in range(min_len):
        if chain_a[i] == fork_point and (i + 1 >= len(chain_a) or i + 1 >= len(chain_b) or chain_a[i + 1] != chain_b[i + 1]):
            fork_index = i
            break

blocks_after_a = len(chain_a) - fork_index - 1
blocks_after_b = len(chain_b) - fork_index - 1

# Determine which chain is longer
if blocks_after_a > blocks_after_b:
    longer = "A"
elif blocks_after_b > blocks_after_a:
    longer = "B"
else:
    longer = "EQUAL"

# Output
print(fork_point)
print(longer)
print(f"A:{blocks_after_a} B:{blocks_after_b}")