import sys

# Read the bid
bid_line = input().strip().split()
bid_count = int(bid_line[0])
bid_face = int(bid_line[1])

# Count the actual occurrences of the bid face
actual_count = 0

# Read all dice sets until EOF
for line in sys.stdin:
    dice = list(map(int, line.strip().split()))
    actual_count += dice.count(bid_face)

# Determine if the bid stands or is a lie
if actual_count >= bid_count:
    print(f"Bid stands: actual count {actual_count}")
else:
    print(f"Liar! actual count {actual_count}")