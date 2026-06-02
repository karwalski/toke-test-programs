n = int(input())
k = int(input())

# Create a list of people numbered 1 to n
people = list(range(1, n + 1))
elimination_order = []
current_pos = 0

# Eliminate people one by one
while len(people) > 1:
    # Find the position of the person to eliminate
    # We need to move k-1 positions from current position
    current_pos = (current_pos + k - 1) % len(people)
    
    # Remove the person at current position and add to elimination order
    eliminated = people.pop(current_pos)
    elimination_order.append(eliminated)
    
    # After removal, current_pos might be out of bounds, so adjust
    if current_pos >= len(people):
        current_pos = 0

# The last remaining person is the survivor
survivor = people[0]

# Output the results
print("Elimination order:", " ".join(map(str, elimination_order)))
print("Survivor:", survivor)