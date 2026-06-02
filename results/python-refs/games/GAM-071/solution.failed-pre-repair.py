import json
import sys

def parse_card(card_str):
    if len(card_str) != 2:
        return None
    rank = card_str[0]
    suit = card_str[1]
    return (rank, suit)

def get_card_value(rank):
    if rank == 'A':
        return 1
    elif rank in '23456789':
        return int(rank)
    elif rank == 'T':
        return 10
    elif rank == 'J':
        return 11
    elif rank == 'Q':
        return 12
    elif rank == 'K':
        return 13
    return 0

def is_red_suit(suit):
    return suit in 'HD'

def is_black_suit(suit):
    return suit in 'SC'

def can_place_on_tableau(card_to_place, card_on_top):
    if card_on_top is None:
        # Can only place King on empty tableau column
        return get_card_value(card_to_place[0]) == 13
    
    rank_to_place = card_to_place[0]
    suit_to_place = card_to_place[1]
    rank_on_top = card_on_top[0]
    suit_on_top = card_on_top[1]
    
    value_to_place = get_card_value(rank_to_place)
    value_on_top = get_card_value(rank_on_top)
    
    # Must be one rank lower and opposite color
    if value_to_place != value_on_top - 1:
        return False
    
    if is_red_suit(suit_to_place) and is_red_suit(suit_on_top):
        return False
    if is_black_suit(suit_to_place) and is_black_suit(suit_on_top):
        return False
    
    return True

def solve_klondike():
    input_lines = []
    for line in sys.stdin:
        input_lines.append(line.rstrip('\n'))
    
    # Find the blank line that separates board state from moves
    blank_line_idx = -1
    for i, line in enumerate(input_lines):
        if line == '':
            blank_line_idx = i
            break
    
    if blank_line_idx == -1:
        # No blank line found, assume all lines are board state
        board_json = ''.join(input_lines)
        moves = []
    else:
        board_json = ''.join(input_lines[:blank_line_idx])
        moves = input_lines[blank_line_idx + 1:]
    
    # Parse board state
    try:
        board_state = json.loads(board_json)
    except:
        return
    
    tableau = board_state.get('tableau', [])
    
    # Process each move
    for move in moves:
        if not move.strip():
            continue
            
        # Parse move (e.g., "col2 to col1")
        parts = move.strip().split()
        if len(parts) != 3 or parts[1] != 'to':
            print("Invalid: malformed move")
            return
        
        from_col = parts[0]
        to_col = parts[2]
        
        # Extract column numbers
        if not from_col.startswith('col') or not to_col.startswith('col'):
            print("Invalid: invalid column reference")
            return
        
        try:
            from_num = int(from_col[3:]) - 1  # Convert to 0-based index
            to_num = int(to_col[3:]) - 1
        except:
            print("Invalid: invalid column number")
            return
        
        # Validate column numbers
        if from_num < 0 or from_num >= len(tableau):
            print("Invalid: source column does not exist")
            return
        if to_num < 0 or to_num >= len(tableau):
            print("Invalid: destination column does not exist")
            return
        
        if from_num == to_num:
            print("Invalid: cannot move to same column")
            return
        
        # Check if source column has cards
        if len(tableau[from_num]) == 0:
            print("Invalid: source column is empty")
            return
        
        # Get the card to move (top card from source column)
        card_to_move_str = tableau[from_num][-1]
        card_to_move = parse_card(card_to_move_str)
        if card_to_move is None:
            print("Invalid: invalid card")
            return
        
        # Get the top card of destination column (if any)
        top_card_dest = None
        if len(tableau[to_num]) > 0:
            top_card_dest_str = tableau[to_num][-1]
            top_card_dest = parse_card(top_card_dest_str)
            if top_card_dest is None:
                print("Invalid: invalid card")
                return
        
        # Check if move is legal
        if can_place_on_tableau(card_to_move, top_card_dest):
            # Execute the move
            tableau[from_num].pop()
            tableau[to_num].append(card_to_move_str)
            print("Valid")
        else:
            print("Invalid: illegal move")
            return

solve_klondike()