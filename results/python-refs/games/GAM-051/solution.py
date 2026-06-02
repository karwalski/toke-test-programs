def calculate_dice_probability(n_dice, n_sides):
    # Total number of outcomes
    total_outcomes = n_sides ** n_dice
    
    # Dictionary to store count of each sum
    sum_counts = {}
    
    # Generate all possible combinations using recursive approach
    def generate_combinations(dice_left, current_sum):
        if dice_left == 0:
            sum_counts[current_sum] = sum_counts.get(current_sum, 0) + 1
            return
        
        for face in range(1, n_sides + 1):
            generate_combinations(dice_left - 1, current_sum + face)
    
    generate_combinations(n_dice, 0)
    
    # Calculate and print probabilities
    for dice_sum in sorted(sum_counts.keys()):
        probability = (sum_counts[dice_sum] / total_outcomes) * 100
        print(f"{dice_sum}: {probability:.2f}%")

# Read input
n_dice, n_sides = map(int, input().split())
calculate_dice_probability(n_dice, n_sides)