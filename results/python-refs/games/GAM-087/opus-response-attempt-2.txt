import sys

def solve_spelling_bee():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    center_letter = lines[0].upper()
    other_letters = lines[1].upper()
    all_letters = set(center_letter + other_letters)
    
    valid_words = []
    
    for i in range(2, len(lines)):
        word = lines[i].upper()
        
        if len(word) < 3:
            continue
        
        if center_letter not in word:
            continue
            
        word_letters = set(word)
        if not word_letters.issubset(all_letters):
            continue
            
        score = len(word)
        if len(word) >= 7 and len(all_letters) == 7 and word_letters == all_letters:
            score += 7
        
        valid_words.append((word, score))
    
    valid_words.sort(key=lambda x: (-len(x[0]), x[0]))
    
    out = []
    for word, score in valid_words:
        out.append(f"{word} ({score})")
    print("\n".join(out))

if __name__ == "__main__":
    solve_spelling_bee()