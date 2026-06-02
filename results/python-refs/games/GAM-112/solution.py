import sys
from itertools import combinations, product

def score_dice(dice, category):
    """Calculate score for given dice and category"""
    dice = sorted(dice)
    
    if category == "Large Straight":
        # Large straight: 5 consecutive numbers (1,2,3,4,5 or 2,3,4,5,6)
        if dice == [1,2,3,4,5] or dice == [2,3,4,5,6]:
            return 40
        return 0
    
    elif category == "Small Straight":
        # Small straight: 4 consecutive numbers
        dice_set = set(dice)
        straights = [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}]
        for straight in straights:
            if straight.issubset(dice_set):
                return 30
        return 0
    
    elif category == "Full House":
        # Full house: 3 of one kind + 2 of another
        counts = {}
        for d in dice:
            counts[d] = counts.get(d, 0) + 1
        count_vals = sorted(counts.values())
        if count_vals == [2, 3]:
            return 25
        return 0
    
    elif category == "Yahtzee":
        # Yahtzee: all 5 dice the same
        if len(set(dice)) == 1:
            return 50
        return 0
    
    elif category == "Chance":
        # Chance: sum of all dice
        return sum(dice)
    
    elif category == "Ones":
        return dice.count(1) * 1
    elif category == "Twos":
        return dice.count(2) * 2
    elif category == "Threes":
        return dice.count(3) * 3
    elif category == "Fours":
        return dice.count(4) * 4
    elif category == "Fives":
        return dice.count(5) * 5
    elif category == "Sixes":
        return dice.count(6) * 6
    
    elif category == "3 of a Kind":
        counts = {}
        for d in dice:
            counts[d] = counts.get(d, 0) + 1
        if max(counts.values()) >= 3:
            return sum(dice)
        return 0
    
    elif category == "4 of a Kind":
        counts = {}
        for d in dice:
            counts[d] = counts.get(d, 0) + 1
        if max(counts.values()) >= 4:
            return sum(dice)
        return 0
    
    return 0

def calculate_expected_value(kept_dice, num_rerolls, category):
    """Calculate expected value when keeping certain dice and rerolling others"""
    if num_rerolls == 0:
        return score_dice(kept_dice, category)
    
    total_value = 0
    total_outcomes = 6 ** num_rerolls
    
    # Generate all possible outcomes for rerolled dice
    for outcome in product(range(1, 7), repeat=num_rerolls):
        final_dice = kept_dice + list(outcome)
        total_value += score_dice(final_dice, category)
    
    return total_value / total_outcomes

def get_subset_description(original_dice, kept_indices):
    """Generate description of what dice are kept/dropped"""
    if len(kept_indices) == len(original_dice):
        return "Keep all"
    
    dropped_indices = [i for i in range(len(original_dice)) if i not in kept_indices]
    if len(dropped_indices) == 1:
        dropped_value = original_dice[dropped_indices[0]]
        return f"Drop {dropped_value}"
    else:
        dropped_values = [str(original_dice[i]) for i in dropped_indices]
        return f"Drop {','.join(dropped_values)}"

def main():
    lines = sys.stdin.read().strip().split('\n')
    dice_line = lines[0]
    category = lines[1]
    
    dice = list(map(int, dice_line.split()))
    
    results = []
    
    # Generate all possible subsets of dice to keep
    for keep_count in range(len(dice), -1, -1):
        for kept_indices in combinations(range(len(dice)), keep_count):
            kept_dice = [dice[i] for i in kept_indices]
            num_rerolls = len(dice) - len(kept_dice)
            
            ev = calculate_expected_value(kept_dice, num_rerolls, category)
            description = get_subset_description(dice, kept_indices)
            
            results.append((ev, description))
    
    # Sort by expected value (descending) and output
    results.sort(key=lambda x: -x[0])
    
    for ev, desc in results:
        print(f"{desc}: EV {ev:.2f}")

if __name__ == "__main__":
    main()