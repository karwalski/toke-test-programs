import random
import re

def parse_dice_expression(expr):
    # Remove spaces
    expr = expr.replace(' ', '')
    
    # Parse the dice notation using regex
    # Pattern: (number)d(sides)(+/-)(modifier)
    pattern = r'(\d+)d(\d+)([+-]\d+)?'
    match = re.match(pattern, expr)
    
    if not match:
        raise ValueError(f"Invalid dice expression: {expr}")
    
    num_dice = int(match.group(1))
    num_sides = int(match.group(2))
    modifier_str = match.group(3) or "+0"
    modifier = int(modifier_str)
    
    return num_dice, num_sides, modifier

def roll_dice(num_dice, num_sides, seed):
    random.seed(seed)
    rolls = []
    for _ in range(num_dice):
        roll = random.randint(1, num_sides)
        rolls.append(roll)
    return rolls

def format_output(rolls, modifier):
    rolls_str = str(rolls).replace(' ', '')
    
    if modifier >= 0:
        modifier_str = f" + {modifier}"
    else:
        modifier_str = f" - {abs(modifier)}"
    
    total = sum(rolls) + modifier
    
    return f"{rolls_str}{modifier_str} = {total}"

# Read input
line = input().strip()
parts = line.split()
dice_expr = parts[0]
seed = int(parts[1])

# Parse and evaluate
num_dice, num_sides, modifier = parse_dice_expression(dice_expr)
rolls = roll_dice(num_dice, num_sides, seed)
output = format_output(rolls, modifier)

print(output)