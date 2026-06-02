import sys

def solve_ghost():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    current = lines[0]
    dictionary = set(lines[1:])
    
    # Find all possible next letters
    possible_letters = set()
    for word in dictionary:
        if word.startswith(current) and len(word) > len(current):
            possible_letters.add(word[len(current)])
    
    def is_winning_move(letter):
        new_string = current + letter
        
        # If this completes a word and no extensions possible, opponent loses
        if new_string in dictionary:
            # Check if any words extend beyond this
            has_extensions = any(word.startswith(new_string) and len(word) > len(new_string) 
                               for word in dictionary)
            if not has_extensions:
                return True
        
        # Find opponent's possible moves
        opponent_moves = set()
        for word in dictionary:
            if word.startswith(new_string) and len(word) > len(new_string):
                opponent_moves.add(word[len(new_string)])
        
        if not opponent_moves:
            return False  # No moves for opponent, but this shouldn't happen
        
        # If all opponent moves are losing for them, this is winning for us
        for opp_letter in opponent_moves:
            opp_string = new_string + opp_letter
            if opp_string in dictionary:
                has_ext = any(word.startswith(opp_string) and len(word) > len(opp_string)
                             for word in dictionary)
                if not has_ext:
                    continue  # This opponent move loses for them
            # If we get here, opponent has at least one non-immediately-losing move
            return False
        
        return True
    
    winning_moves = []
    losing_moves = []
    
    for letter in sorted(possible_letters):
        if is_winning_move(letter):
            winning_moves.append(letter)
        else:
            losing_moves.append(letter)
    
    print("Winning moves:", " ".join(winning_moves))
    print("Losing moves:", " ".join(losing_moves))

solve_ghost()