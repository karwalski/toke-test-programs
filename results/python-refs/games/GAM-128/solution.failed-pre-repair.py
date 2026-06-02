import sys
from collections import defaultdict
import time

def solve_codeword():
    start_time = time.time()
    
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse grid
    grid = []
    i = 0
    while i < len(lines) and not '=' in lines[i]:
        if lines[i]:
            grid.append(list(map(int, lines[i].split())))
        i += 1
    
    # Parse known assignments
    known = {}
    while i < len(lines) and '=' in lines[i]:
        if lines[i]:
            num, letter = lines[i].split('=')
            known[int(num)] = letter
        i += 1
    
    # Parse dictionary
    dictionary = []
    while i < len(lines):
        if lines[i]:
            dictionary.append(lines[i].upper())
        i += 1
    
    rows, cols = len(grid), len(grid[0])
    
    # Find all horizontal and vertical words in grid
    words_positions = []
    
    # Horizontal words
    for r in range(rows):
        word_start = 0
        for c in range(cols + 1):
            if c == cols or (c > 0 and grid[r][c] == 0):  # Word boundary
                if c - word_start >= 2:  # Only words of length 2 or more
                    positions = [(r, col) for col in range(word_start, c)]
                    words_positions.append(positions)
                word_start = c + 1
    
    # Vertical words
    for c in range(cols):
        word_start = 0
        for r in range(rows + 1):
            if r == rows or (r > 0 and grid[r][c] == 0):  # Word boundary
                if r - word_start >= 2:  # Only words of length 2 or more
                    positions = [(row, c) for row in range(word_start, r)]
                    words_positions.append(positions)
                word_start = r + 1
    
    # Group dictionary words by length
    words_by_length = defaultdict(list)
    for word in dictionary:
        words_by_length[len(word)].append(word)
    
    # Initialize assignments
    num_to_letter = known.copy()
    letter_to_num = {v: k for k, v in known.items()}
    
    def is_valid_assignment(positions, word):
        # Check if assigning this word to these positions is consistent
        temp_num_to_letter = num_to_letter.copy()
        temp_letter_to_num = letter_to_num.copy()
        
        for pos, letter in zip(positions, word):
            num = grid[pos[0]][pos[1]]
            
            # Check if number already assigned to different letter
            if num in temp_num_to_letter and temp_num_to_letter[num] != letter:
                return False
            
            # Check if letter already assigned to different number
            if letter in temp_letter_to_num and temp_letter_to_num[letter] != num:
                return False
            
            temp_num_to_letter[num] = letter
            temp_letter_to_num[letter] = num
        
        return True
    
    def apply_assignment(positions, word):
        for pos, letter in zip(positions, word):
            num = grid[pos[0]][pos[1]]
            num_to_letter[num] = letter
            letter_to_num[letter] = num
    
    def remove_assignment(positions, word):
        for pos, letter in zip(positions, word):
            num = grid[pos[0]][pos[1]]
            if num not in known:  # Don't remove known assignments
                if num in num_to_letter:
                    del num_to_letter[num]
                if letter in letter_to_num:
                    del letter_to_num[letter]
    
    def is_partial_match(positions, word):
        # Check if current partial assignment is consistent with this word
        for pos, letter in zip(positions, word):
            num = grid[pos[0]][pos[1]]
            if num in num_to_letter and num_to_letter[num] != letter:
                return False
        return True
    
    def backtrack(word_idx):
        if time.time() - start_time > 7:  # Time limit
            return False
            
        if word_idx >= len(words_positions):
            return True
        
        positions = words_positions[word_idx]
        word_length = len(positions)
        
        # Get possible words for this length
        possible_words = words_by_length[word_length]
        
        # Filter words that match current partial assignment
        valid_words = []
        for word in possible_words:
            if is_partial_match(positions, word):
                valid_words.append(word)
        
        for word in valid_words:
            if is_valid_assignment(positions, word):
                # Save current state
                old_num_to_letter = num_to_letter.copy()
                old_letter_to_num = letter_to_num.copy()
                
                apply_assignment(positions, word)
                
                if backtrack(word_idx + 1):
                    return True
                
                # Restore state
                num_to_letter.clear()
                num_to_letter.update(old_num_to_letter)
                letter_to_num.clear()
                letter_to_num.update(old_letter_to_num)
        
        return False
    
    if backtrack(0):
        # Output solution
        for r in range(rows):
            row_output = []
            for c in range(cols):
                num = grid[r][c]
                if num in num_to_letter:
                    row_output.append(f"{num}={num_to_letter[num]}")
                else:
                    row_output.append(str(num))
            print(' '.join(row_output))
    else:
        print("No solution")

solve_codeword()