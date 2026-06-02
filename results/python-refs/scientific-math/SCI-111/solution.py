def polynomial_hash_2d(matrix, rows, cols, base=256, mod=10**9+7):
    """Compute 2D polynomial hash of a matrix"""
    hash_val = 0
    for i in range(rows):
        for j in range(cols):
            hash_val = (hash_val * base + ord(matrix[i][j])) % mod
    return hash_val

def get_submatrix_hash(text, start_row, start_col, rows, cols, base=256, mod=10**9+7):
    """Get hash of submatrix starting at (start_row, start_col)"""
    hash_val = 0
    for i in range(start_row, start_row + rows):
        for j in range(start_col, start_col + cols):
            hash_val = (hash_val * base + ord(text[i][j])) % mod
    return hash_val

def matrices_equal(text, start_row, start_col, pattern, pattern_rows, pattern_cols):
    """Check if submatrix equals pattern"""
    for i in range(pattern_rows):
        for j in range(pattern_cols):
            if text[start_row + i][start_col + j] != pattern[i][j]:
                return False
    return True

def rabin_karp_2d(text, pattern):
    text_rows = len(text)
    text_cols = len(text[0])
    pattern_rows = len(pattern)
    pattern_cols = len(pattern[0])
    
    if pattern_rows > text_rows or pattern_cols > text_cols:
        return []
    
    base = 256
    mod = 10**9 + 7
    
    # Compute pattern hash
    pattern_hash = polynomial_hash_2d(pattern, pattern_rows, pattern_cols, base, mod)
    
    matches = []
    
    # Check all possible positions
    for i in range(text_rows - pattern_rows + 1):
        for j in range(text_cols - pattern_cols + 1):
            # Compute hash of current submatrix
            submatrix_hash = get_submatrix_hash(text, i, j, pattern_rows, pattern_cols, base, mod)
            
            # If hashes match, verify with actual comparison
            if submatrix_hash == pattern_hash:
                if matrices_equal(text, i, j, pattern, pattern_rows, pattern_cols):
                    matches.append((i, j))
    
    return matches

# Read input
line1 = input().split()
text_rows, text_cols = int(line1[0]), int(line1[1])

text = []
for _ in range(text_rows):
    text.append(input().strip())

line2 = input().split()
pattern_rows, pattern_cols = int(line2[0]), int(line2[1])

pattern = []
for _ in range(pattern_rows):
    pattern.append(input().strip())

# Find matches
matches = rabin_karp_2d(text, pattern)

# Output results
for row, col in matches:
    print(f"Found at: ({row},{col})")
print(f"Count: {len(matches)}")