def calculate_nim_sum(piles):
    result = 0
    for pile in piles:
        result ^= pile
    return result

def find_optimal_move(piles):
    nim_sum = calculate_nim_sum(piles)
    if nim_sum == 0:
        return "Losing position"
    for i in range(len(piles) - 1, -1, -1):
        pile_size = piles[i]
        target_size = pile_size ^ nim_sum
        if target_size < pile_size:
            stones_to_take = pile_size - target_size
            return f"Take {stones_to_take} from pile {i + 1}"
    return "Losing position"

line = input().strip()
piles = list(map(int, line.split()))
print(find_optimal_move(piles))