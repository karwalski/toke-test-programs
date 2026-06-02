In test 1, the grid is:
```
CAT
#A#
SAT
```
Column 1 is "AAA" (length 3). But expected invalid is "AA". So the validation must check if extracted words are in the answer list. "AAA" not in list → invalid. But expected is "AA"...

Wait, maybe the comparison is reversed: check if all words in the answer list appear in the grid. Answer list is CAT, SAT, AA. "AA" not in grid → invalid.

Let me verify test 2: list is CAT, SAT. Both in grid → Valid. ✓
Test 1: AA not in grid words {CAT, SAT, AAA} → Invalid: AA. ✓

```python
import sys

def extract_words_from_grid(grid):
    words = set()
    rows = len(grid)
    cols = max((len(r) for r in grid), default=0)
    
    for i in range(rows):
        current_word = ""
        for j in range(len(grid[i])):
            if grid[i][j] != '#':
                current_word += grid[i][j]
            else:
                if len(current_word) > 1:
                    words.add(current_word)
                current_word = ""
        if len(current_word) > 1:
            words.add(current_word)
    
    for j in range(cols):
        current_word = ""
        for i in range(rows):
            if j < len(grid[i]) and grid[i][j] != '#':
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
    
    blank_line_idx = -1
    for i, line in enumerate(lines):
        if line == "":
            blank_line_idx = i
            break
    
    if blank_line_idx == -1:
        grid_lines = lines
        word_list = []
    else:
        grid_lines = lines[:blank_line_idx]
        word_list = [l for l in lines[blank_line_idx + 1:] if l]
    
    grid = [list(line) for line in grid_lines if line]
    
    extracted_words = extract_words_from_grid(grid)
    
    invalid = [w for w in word_list if w not in extracted_words]
    
    if not invalid:
        print("Valid")
    else:
        print("Invalid: " + ", ".join(invalid))

if __name__ == "__main__":
    main()
```