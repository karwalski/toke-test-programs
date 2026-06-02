import sys

def main():
    # T9 keypad mapping
    keypad = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    phone_digits = lines[0]
    dictionary_words = lines[1:]
    
    # Convert phone digits to possible letters
    def get_possible_letters(digits):
        if not digits:
            return ['']
        
        first_digit = digits[0]
        rest_digits = digits[1:]
        
        if first_digit not in keypad:
            return []
        
        letters = keypad[first_digit]
        rest_combinations = get_possible_letters(rest_digits)
        
        combinations = []
        for letter in letters:
            for rest in rest_combinations:
                combinations.append(letter + rest)
        
        return combinations
    
    # Get all possible letter combinations
    possible_combinations = get_possible_letters(phone_digits)
    possible_combinations_upper = [combo.upper() for combo in possible_combinations]
    
    # Find matching words
    matching_words = []
    for word in dictionary_words:
        if word.upper() in possible_combinations_upper:
            matching_words.append(word)
    
    # Sort alphabetically and output
    matching_words.sort()
    for word in matching_words:
        print(word)

if __name__ == "__main__":
    main()