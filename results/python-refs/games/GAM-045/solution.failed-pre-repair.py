import sys

def extract_words_from_grid(grid):
    words = set()
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Extract horizontal words
    for i in range(rows):
        current_word = ""
        for j in range(cols):
            if grid[i][j] != '#':
                current_word += grid[i][j]
            else:
                if len(current_word) > 1:
                    words.add(current_word)
                current_word = ""
        if len(current_word) > 1:
            words.add(current_word)
    
    # Extract vertical words
    for j in range(cols):
        current_word = ""
        for i in range(rows):
            if grid[i][j] != '#':
                current_word += grid[i][j]
            else:
                if len(current_word) > 1:
                    words.add(current_word)
                current_word = ""
        if len(current_word) > 1:
            words.add(current_word)
    
    return words

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the blank line separating grid from word list
    blank_line_idx = -1
    for i, line in enumerate(lines):
        if line == "":
            blank_line_idx = i
            break
    
    if blank_line_idx == -1:
        # No blank line found, assume all lines are grid
        grid_lines = lines
        word_list = []
    else:
        grid_lines = lines[:blank_line_idx]
        word_list = lines[blank_line_idx + 1:]
    
    # Parse grid
    grid = [list(line) for line in grid_lines if line]
    
    # Extract words from grid
    extracted_words = extract_words_from_grid(grid)
    
    # Create set of valid words
    valid_words = set(word_list)
    
    # Find invalid words
    invalid_words = extracted_words - valid_words
    
    if not invalid_words:
        print("Valid")
    else:
        invalid_list = sorted(invalid_words)
        print("Invalid: " + ", ".join(invalid_list))

if __name__ == "__main__":
    main()