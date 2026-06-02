import sys

def check_word_against_feedback(word, guess, feedback):
    """Check if a word is consistent with the given guess and feedback."""
    if len(word) != len(guess) or len(word) != len(feedback):
        return False
    
    word = word.upper()
    guess = guess.upper()
    feedback = feedback.upper()
    
    # Track which letters are confirmed to be in the target word
    confirmed_letters = {}
    excluded_letters = set()
    
    # First pass: handle G (correct position) and collect B (not in word)
    for i, (g_char, f_char) in enumerate(zip(guess, feedback)):
        if f_char == 'G':
            if word[i] != g_char:
                return False
            confirmed_letters[g_char] = confirmed_letters.get(g_char, 0) + 1
        elif f_char == 'B':
            # This letter is not in the target word at all
            excluded_letters.add(g_char)
    
    # Second pass: handle Y (wrong position)
    for i, (g_char, f_char) in enumerate(zip(guess, feedback)):
        if f_char == 'Y':
            # Letter must be in the word but not at this position
            if word[i] == g_char:
                return False
            # Count occurrences of this letter in the word
            if g_char not in word:
                return False
            confirmed_letters[g_char] = confirmed_letters.get(g_char, 0) + 1
    
    # Check that excluded letters are not in the word
    # Exception: if a letter has both B and G/Y feedback, it means
    # the letter appears exactly as many times as G/Y indicate
    for letter in excluded_letters:
        if letter in confirmed_letters:
            # Count exact occurrences in word
            word_count = word.count(letter)
            required_count = confirmed_letters[letter]
            if word_count != required_count:
                return False
        else:
            # Letter should not appear in word at all
            if letter in word:
                return False
    
    # Verify all confirmed letters appear with correct frequency
    for letter, required_count in confirmed_letters.items():
        if word.count(letter) < required_count:
            return False
    
    return True

def solve_wordle():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the blank line separator
    blank_line_idx = -1
    for i, line in enumerate(lines):
        if line == '':
            blank_line_idx = i
            break
    
    if blank_line_idx == -1:
        # No feedback provided, return first word
        if lines:
            print(lines[0])
        return
    
    # Parse word list and feedback
    word_list = [line.strip() for line in lines[:blank_line_idx] if line.strip()]
    feedback_lines = [line.strip() for line in lines[blank_line_idx + 1:] if line.strip()]
    
    # Parse guess:feedback pairs
    guesses_feedback = []
    for line in feedback_lines:
        if ':' in line:
            guess, feedback = line.split(':', 1)
            guesses_feedback.append((guess.strip(), feedback.strip()))
    
    # Filter words that are consistent with all feedback
    valid_words = []
    for word in word_list:
        is_valid = True
        for guess, feedback in guesses_feedback:
            if not check_word_against_feedback(word, guess, feedback):
                is_valid = False
                break
        if is_valid:
            valid_words.append(word)
    
    # Return the first valid word (best guess)
    if valid_words:
        print(valid_words[0])
    elif word_list:
        print(word_list[0])

if __name__ == "__main__":
    solve_wordle()