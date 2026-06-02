dice = list(map(int, input().split()))
category = input().strip()

def calculate_score(dice, category):
    dice_counts = {}
    for die in dice:
        dice_counts[die] = dice_counts.get(die, 0) + 1
    
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
        for count in dice_counts.values():
            if count >= 3:
                return sum(dice)
        return 0
    elif category == "Four of a Kind":
        for count in dice_counts.values():
            if count >= 4:
                return sum(dice)
        return 0
    elif category == "Full House":
        counts = sorted(dice_counts.values())
        if counts == [2, 3]:
            return 25
        return 0
    elif category == "Small Straight":
        unique_dice = set(dice)
        straights = [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}]
        for straight in straights:
            if straight.issubset(unique_dice):
                return 30
        return 0
    elif category == "Large Straight":
        unique_dice = set(dice)
        if unique_dice == {1,2,3,4,5} or unique_dice == {2,3,4,5,6}:
            return 40
        return 0
    elif category == "Yahtzee":
        for count in dice_counts.values():
            if count == 5:
                return 50
        return 0
    elif category == "Chance":
        return sum(dice)
    
    return 0

print(calculate_score(dice, category))