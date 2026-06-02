import json
import sys

# Read input
total_supply = int(input().strip())
quorum_percent = int(input().strip())
votes_json = input().strip()

# Parse votes
votes = json.loads(votes_json)

# Calculate vote totals
for_votes = 0
against_votes = 0
abstain_votes = 0

for vote in votes:
    tokens = vote["tokens"]
    choice = vote["choice"]
    
    if choice == "for":
        for_votes += tokens
    elif choice == "against":
        against_votes += tokens
    elif choice == "abstain":
        abstain_votes += tokens

# Calculate total votes and check quorum
total_votes = for_votes + against_votes + abstain_votes
quorum_threshold = (total_supply * quorum_percent) / 100

# Determine result
if total_votes < quorum_threshold:
    result = "NO_QUORUM"
elif for_votes > against_votes:
    result = "PASSED"
else:
    result = "FAILED"

# Output
print(result)
print(f"for:{for_votes} against:{against_votes} abstain:{abstain_votes}")