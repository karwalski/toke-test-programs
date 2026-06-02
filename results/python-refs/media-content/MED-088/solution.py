import sys

def translate_to_pig_latin(word):
    if not word:
        return word
    
    vowels = 'aeiouAEIOU'
    
    if word[0] in vowels:
        return word + 'way'
    else:
        return word[1:] + word[0] + 'ay'

def main():
    text = sys.stdin.read().strip()
    words = text.split()
    pig_latin_words = [translate_to_pig_latin(word) for word in words]
    print(' '.join(pig_latin_words))

if __name__ == "__main__":
    main()