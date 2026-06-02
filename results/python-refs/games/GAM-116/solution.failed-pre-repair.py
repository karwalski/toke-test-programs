import random

def generate_bingo_card(seed):
    random.seed(seed)
    
    # Standard Bingo ranges for each column
    b_nums = list(range(1, 16))   # B: 1-15
    i_nums = list(range(16, 31))  # I: 16-30
    n_nums = list(range(31, 46))  # N: 31-45
    g_nums = list(range(46, 61))  # G: 46-60
    o_nums = list(range(61, 76))  # O: 61-75
    
    # Shuffle each column's numbers
    random.shuffle(b_nums)
    random.shuffle(i_nums)
    random.shuffle(n_nums)
    random.shuffle(g_nums)
    random.shuffle(o_nums)
    
    # Create 5x5 card
    card = []
    for row in range(5):
        card_row = []
        card_row.append(b_nums[row])
        card_row.append(i_nums[row])
        if row == 2:  # Middle cell is FREE
            card_row.append(0)  # Use 0 to represent FREE space
        else:
            card_row.append(n_nums[row])
        card_row.append(g_nums[row])
        card_row.append(o_nums[row])
        card.append(card_row)
    
    return card

def check_bingo(card, marked):
    # Check rows
    for i in range(5):
        if all(card[i][j] == 0 or card[i][j] in marked for j in range(5)):
            return f"Row {i + 1} complete"
    
    # Check columns
    for j in range(5):
        if all(card[i][j] == 0 or card[i][j] in marked for i in range(5)):
            return f"Column {j + 1} complete"
    
    # Check diagonals
    if all(card[i][i] == 0 or card[i][i] in marked for i in range(5)):
        return "Diagonal complete"
    
    if all(card[i][4-i] == 0 or card[i][4-i] in marked for i in range(5)):
        return "Diagonal complete"
    
    return None

def main():
    lines = []
    try:
        while True:
            line = input().strip()
            if line:
                lines.append(line)
    except EOFError:
        pass
    
    seed = int(lines[0])
    called_numbers = []
    
    # Parse called numbers
    for i in range(1, len(lines)):
        numbers = lines[i].split()
        called_numbers.extend([int(x) for x in numbers])
    
    # Generate card
    card = generate_bingo_card(seed)
    
    # Check for bingo as numbers are called
    marked = set()
    marked.add(0)  # FREE space is always marked
    
    for num in called_numbers:
        marked.add(num)
        win_condition = check_bingo(card, marked)
        if win_condition:
            print(f"Bingo! {win_condition} after calling {num}")
            return
    
    print("No bingo")

if __name__ == "__main__":
    main()