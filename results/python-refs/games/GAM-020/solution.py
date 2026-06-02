import sys
from collections import Counter

def calculate_score(dice, category):
    dice_counts = Counter(dice)
    
    if category == "Ones":
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
    elif category == "Three of a Kind":
        for value, count in dice_counts.items():
            if count >= 3:
                return sum(dice)
        return 0
    elif category == "Four of a Kind":
        for value, count in dice_counts.items():
            if count >= 4:
                return sum(dice)
        return 0
    elif category == "Full House":
        counts = sorted(dice_counts.values())
        if counts == [2, 3]:
            return 25
        return 0
    elif category == "Small Straight":
        dice_set = set(dice)
        straights = [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}]
        for straight in straights:
            if straight.issubset(dice_set):
                return 30
        return 0
    elif category == "Large Straight":
        dice_set = set(dice)
        if dice_set == {1,2,3,4,5} or dice_set == {2,3,4,5,6}:
            return 40
        return 0
    elif category == "Yahtzee":
        if len(dice_counts) == 1:
            return 50
        return 0
    elif category == "Chance":
        return sum(dice)
    
    return 0

# Read input
dice_line = input().strip()
dice = list(map(int, dice_line.split()))

categories = []
try:
    while True:
        line = input().strip()
        if line:
            categories.append(line)
except EOFError:
    pass

# Find best category
best_category = ""
best_score = -1

for category in categories:
    score = calculate_score(dice, category)
    if score > best_score:
        best_score = score
        best_category = category

print(best_category)