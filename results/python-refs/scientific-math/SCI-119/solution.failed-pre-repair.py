def gale_shapley(n, proposer_prefs, acceptor_prefs):
    # Create preference rankings for faster lookup
    acceptor_rankings = []
    for i in range(n):
        ranking = [0] * n
        for rank, proposer in enumerate(acceptor_prefs[i]):
            ranking[proposer] = rank
        acceptor_rankings.append(ranking)
    
    # Initialize variables
    proposer_partner = [-1] * n  # -1 means unmatched
    acceptor_partner = [-1] * n
    proposer_next_proposal = [0] * n  # next person to propose to
    
    # Keep track of free proposers
    free_proposers = list(range(n))
    
    while free_proposers:
        proposer = free_proposers.pop(0)
        
        # Find next acceptor to propose to
        if proposer_next_proposal[proposer] >= n:
            continue
            
        acceptor = proposer_prefs[proposer][proposer_next_proposal[proposer]]
        proposer_next_proposal[proposer] += 1
        
        if acceptor_partner[acceptor] == -1:
            # Acceptor is free, accept the proposal
            proposer_partner[proposer] = acceptor
            acceptor_partner[acceptor] = proposer
        else:
            # Acceptor is already matched, check if prefers this proposer
            current_partner = acceptor_partner[acceptor]
            if acceptor_rankings[acceptor][proposer] < acceptor_rankings[acceptor][current_partner]:
                # Acceptor prefers new proposer
                proposer_partner[proposer] = acceptor
                acceptor_partner[acceptor] = proposer
                proposer_partner[current_partner] = -1
                free_proposers.append(current_partner)
            else:
                # Acceptor prefers current partner, proposer remains free
                free_proposers.append(proposer)
    
    return proposer_partner

def is_stable(n, proposer_prefs, acceptor_prefs, matching):
    # Create preference rankings for faster lookup
    proposer_rankings = []
    for i in range(n):
        ranking = [0] * n
        for rank, acceptor in enumerate(proposer_prefs[i]):
            ranking[acceptor] = rank
        proposer_rankings.append(ranking)
    
    acceptor_rankings = []
    for i in range(n):
        ranking = [0] * n
        for rank, proposer in enumerate(acceptor_prefs[i]):
            ranking[proposer] = rank
        acceptor_rankings.append(ranking)
    
    # Check for blocking pairs
    for proposer in range(n):
        current_acceptor = matching[proposer]
        for acceptor in range(n):
            if acceptor == current_acceptor:
                continue
            
            # Check if proposer prefers acceptor over current partner
            if proposer_rankings[proposer][acceptor] < proposer_rankings[proposer][current_acceptor]:
                # Check if acceptor prefers proposer over current partner
                current_proposer_of_acceptor = -1
                for p in range(n):
                    if matching[p] == acceptor:
                        current_proposer_of_acceptor = p
                        break
                
                if acceptor_rankings[acceptor][proposer] < acceptor_rankings[acceptor][current_proposer_of_acceptor]:
                    return False
    
    return True

# Read input
n = int(input())

proposer_prefs = []
for i in range(n):
    prefs = list(map(int, input().split()))
    proposer_prefs.append(prefs)

acceptor_prefs = []
for i in range(n):
    prefs = list(map(int, input().split()))
    acceptor_prefs.append(prefs)

# Find matching using Gale-Shapley
matching = gale_shapley(n, proposer_prefs, acceptor_prefs)

# Check if matching is stable
stable = is_stable(n, proposer_prefs, acceptor_prefs, matching)

# Output results
pairs = []
for proposer in range(n):
    pairs.append(f"{proposer}-{matching[proposer]}")

print("Matching: " + " ".join(pairs))
print(f"Stable: {str(stable).lower()}")