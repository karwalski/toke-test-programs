def calculate_nim_sum(piles):
    """Calculate the XOR (nim-sum) of all pile sizes"""
    result = 0
    for pile in piles:
        result ^= pile
    return result

def find_optimal_move(piles):
    """Find the optimal move using Sprague-Grundy theorem"""
    nim_sum = calculate_nim_sum(piles)
    
    # If nim-sum is 0, it's a losing position
    if nim_sum == 0:
        return "Losing position"
    
    # Find a move that makes nim-sum = 0
    for i, pile_size in enumerate(piles):
        # Calculate what this pile should be to make nim-sum = 0
        target_size = pile_size ^ nim_sum
        
        # We can only reduce pile sizes, not increase them
        if target_size < pile_size:
            stones_to_take = pile_size - target_size
            pile_number = i + 1  # 1-indexed for output
            return f"Take {stones_to_take} from pile {pile_number}"
    
    # This should never happen if nim_sum != 0
    return "Losing position"

# Read input
line = input().strip()
piles = list(map(int, line.split()))

# Find and print the optimal move
result = find_optimal_move(piles)
print(result)