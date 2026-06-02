import json
import sys

def parse_card(card_str):
    if len(card_str) != 2:
        return None
    return (card_str[0], card_str[1])

def get_card_value(rank):
    if rank == 'A': return 1
    if rank in '23456789': return int(rank)
    if rank == 'T': return 10
    if rank == 'J': return 11
    if rank == 'Q': return 12
    if rank == 'K': return 13
    return 0

def is_red(suit): return suit in 'HD'

def can_place(card, top):
    if top is None:
        return get_card_value(card[0]) == 13
    if get_card_value(card[0]) != get_card_value(top[0]) - 1:
        return False
    if is_red(card[1]) == is_red(top[1]):
        return False
    return True

def main():
    data = sys.stdin.read()
    lines = data.split('\n')
    blank = -1
    for i, l in enumerate(lines):
        if l.strip() == '':
            try:
                json.loads('\n'.join(lines[:i]))
                blank = i
                break
            except:
                continue
    if blank == -1:
        return
    board = json.loads('\n'.join(lines[:blank]))
    moves = [l for l in lines[blank+1:] if l.strip()]
    tableau = board.get('tableau', [])
    
    for move in moves:
        parts = move.strip().split()
        if len(parts) != 3 or parts[1] != 'to':
            print("Invalid: malformed move")
            return
        try:
            f = int(parts[0][3:]) - 1
            t = int(parts[2][3:]) - 1
        except:
            print("Invalid: invalid column")
            return
        if f < 0 or f >= len(tableau) or t < 0 or t >= len(tableau):
            print("Invalid: column does not exist")
            return
        if len(tableau[f]) == 0:
            print("Invalid: source empty")
            return
        card_str = tableau[f][-1]
        card = parse_card(card_str)
        top = parse_card(tableau[t][-1]) if tableau[t] else None
        
        if top is None:
            if get_card_value(card[0]) != 13:
                print("Invalid: only K can go on empty column")
                return
        else:
            if get_card_value(card[0]) == 13:
                print("Invalid: K can only go on empty column")
                return
            if not can_place(card, top):
                print("Invalid: illegal move")
                return
        
        tableau[f].pop()
        tableau[t].append(card_str)
        print("Valid")

main()