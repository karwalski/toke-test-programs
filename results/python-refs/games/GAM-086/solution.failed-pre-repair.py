import sys

def solve_hangman():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    masked_word = lines[0]
    wrong_guesses = set(lines[1].split()) if lines[1] else set()
    dictionary = lines[2:]
    
    # Find known letters from masked word
    known_letters = set()
    for char in masked_word:
        if char != '_':
            known_letters.add(char)
    
    # Filter dictionary to match the pattern
    possible_words = []
    word_length = len(masked_word)
    
    for word in dictionary:
        if len(word) != word_length:
            continue
            
        # Check if word matches the pattern
        matches = True
        for i in range(word_length):
            if masked_word[i] == '_':
                # This position should not be a known letter or wrong guess
                if word[i] in known_letters or word[i] in wrong_guesses:
                    matches = False
                    break
            else:
                # This position should match exactly
                if word[i] != masked_word[i]:
                    matches = False
                    break
        
        if matches:
            # Also check that the word doesn't contain any wrong guesses
            word_contains_wrong = False
            for letter in wrong_guesses:
                if letter in word:
                    word_contains_wrong = True
                    break
            
            if not word_contains_wrong:
                possible_words.append(word)
    
    # Count frequency of each letter in possible words
    letter_count = {}
    used_letters = known_letters | wrong_guesses
    
    for word in possible_words:
        for letter in word:
            if letter not in used_letters:
                letter_count[letter] = letter_count.get(letter, 0) + 1
    
    # Find the letter with highest frequency
    best_letter = max(letter_count.keys(), key=lambda x: letter_count[x])
    
    print(best_letter)

solve_hangman()