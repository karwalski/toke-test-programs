import sys

def get_neighbors(row, col, grid_size=4):
    """Get all valid neighboring positions for a given cell"""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < grid_size and 0 <= new_col < grid_size:
                neighbors.append((new_row, new_col))
    return neighbors

def find_word_in_grid(word, grid):
    """Check if a word can be formed in the grid following Boggle rules"""
    def dfs(word_idx, row, col, visited):
        if word_idx == len(word):
            return True
        
        if (row, col) in visited or grid[row][col] != word[word_idx]:
            return False
        
        visited.add((row, col))
        
        for next_row, next_col in get_neighbors(row, col):
            if dfs(word_idx + 1, next_row, next_col, visited):
                visited.remove((row, col))
                return True
        
        visited.remove((row, col))
        return False
    
    # Try starting from each cell in the grid
    for row in range(4):
        for col in range(4):
            if dfs(0, row, col, set()):
                return True
    return False

def main():
    # Read the grid
    grid = []
    for _ in range(4):
        line = input().strip()
        grid.append(list(line))
    
    # Read blank line
    input()
    
    # Read dictionary words
    words = []
    try:
        while True:
            word = input().strip()
            if word:
                words.append(word)
    except EOFError:
        pass
    
    # Find valid words
    valid_words = []
    for word in words:
        if len(word) >= 3 and find_word_in_grid(word, grid):
            valid_words.append(word)
    
    # Sort by length (descending) then alphabetically
    valid_words.sort(key=lambda x: (-len(x), x))
    
    # Output results
    for word in valid_words:
        print(word)

if __name__ == "__main__":
    main()