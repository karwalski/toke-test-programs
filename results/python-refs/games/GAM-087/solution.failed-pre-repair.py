import sys

def solve_spelling_bee():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    center_letter = lines[0].upper()
    other_letters = lines[1].upper()
    all_letters = set(center_letter + other_letters)
    
    valid_words = []
    
    # Process each word starting from line 2
    for i in range(2, len(lines)):
        word = lines[i].upper()
        
        # Check if word contains center letter
        if center_letter not in word:
            continue
            
        # Check if word only uses allowed letters
        word_letters = set(word)
        if not word_letters.issubset(all_letters):
            continue
            
        # Calculate score
        score = len(word)
        
        valid_words.append((word, score))
    
    # Sort by length descending, then alphabetically
    valid_words.sort(key=lambda x: (-x[1], x[0]))
    
    # Output results
    for word, score in valid_words:
        print(f"{word} ({score})")

if __name__ == "__main__":
    solve_spelling_bee()