import sys

def check_word_against_feedback(word, guess, feedback):
    if len(word) != len(guess) or len(word) != len(feedback):
        return False
    word = word.upper()
    guess = guess.upper()
    feedback = feedback.upper()
    
    confirmed_letters = {}
    excluded_letters = set()
    
    for i, (g_char, f_char) in enumerate(zip(guess, feedback)):
        if f_char == 'G':
            if word[i] != g_char:
                return False
            confirmed_letters[g_char] = confirmed_letters.get(g_char, 0) + 1
        elif f_char == 'B':
            excluded_letters.add(g_char)
    
    for i, (g_char, f_char) in enumerate(zip(guess, feedback)):
        if f_char == 'Y':
            if word[i] == g_char:
                return False
            if g_char not in word:
                return False
            confirmed_letters[g_char] = confirmed_letters.get(g_char, 0) + 1
    
    for letter in excluded_letters:
        if letter in confirmed_letters:
            word_count = word.count(letter)
            required_count = confirmed_letters[letter]
            if word_count != required_count:
                return False
        else:
            if letter in word:
                return False
    
    for letter, required_count in confirmed_letters.items():
        if word.count(letter) < required_count:
            return False
    
    return True

def compute_entropy(candidate, valid_words):
    from collections import Counter
    from math import log2
    if not valid_words:
        return 0
    patterns = Counter()
    for target in valid_words:
        pattern = compute_pattern(candidate, target)
        patterns[pattern] += 1
    total = len(valid_words)
    entropy = 0
    for count in patterns.values():
        p = count / total
        entropy -= p * log2(p)
    return entropy

def compute_pattern(guess, target):
    guess = guess.upper()
    target = target.upper()
    result = ['B'] * len(guess)
    target_chars = list(target)
    for i in range(len(guess)):
        if guess[i] == target_chars[i]:
            result[i] = 'G'
            target_chars[i] = None
    for i in range(len(guess)):
        if result[i] == 'B' and guess[i] in target_chars:
            result[i] = 'Y'
            target_chars[target_chars.index(guess[i])] = None
    return ''.join(result)

def solve_wordle():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    blank_line_idx = -1
    for i, line in enumerate(lines):
        if line == '':
            blank_line_idx = i
            break
    
    if blank_line_idx == -1:
        word_list = [line.strip() for line in lines if line.strip()]
        if word_list:
            print(word_list[0])
        return
    
    word_list = [line.strip() for line in lines[:blank_line_idx] if line.strip()]
    feedback_lines = [line.strip() for line in lines[blank_line_idx + 1:] if line.strip()]
    
    guesses_feedback = []
    for line in feedback_lines:
        if ':' in line:
            guess, feedback = line.split(':', 1)
            guesses_feedback.append((guess.strip(), feedback.strip()))
    
    valid_words = []
    for word in word_list:
        is_valid = True
        for guess, feedback in guesses_feedback:
            if not check_word_against_feedback(word, guess, feedback):
                is_valid = False
                break
        if is_valid:
            valid_words.append(word)
    
    if not valid_words:
        if word_list:
            print(word_list[0])
        return
    
    if len(valid_words) == 1 or not guesses_feedback:
        print(valid_words[0])
        return
    
    best_word = valid_words[0]
    best_entropy = -1
    for candidate in valid_words:
        entropy = compute_entropy(candidate, valid_words)
        if entropy > best_entropy:
            best_entropy = entropy
            best_word = candidate
    
    print(best_word)

if __name__ == "__main__":
    solve_wordle()