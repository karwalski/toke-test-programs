import sys

def main():
    keypad = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    phone_digits = lines[0]
    dictionary_words = lines[1:]
    
    def word_to_digits(word):
        result = ''
        for ch in word.lower():
            for digit, letters in keypad.items():
                if ch in letters:
                    result += digit
                    break
            else:
                return None
        return result
    
    matching = []
    for word in dictionary_words:
        if word_to_digits(word) == phone_digits:
            matching.append(word.upper())
    
    matching.sort()
    for word in matching:
        print(word)

if __name__ == "__main__":
    main()