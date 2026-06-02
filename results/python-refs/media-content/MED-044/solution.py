import sys

def to_title_case(text):
    # Words that should be lowercase in AP style (except at beginning/end)
    lowercase_words = {
        'a', 'an', 'and', 'at', 'but', 'by', 'for', 'in', 'nor', 'of', 
        'on', 'or', 'so', 'the', 'to', 'up', 'yet'
    }
    
    words = text.split()
    if not words:
        return text
    
    result = []
    
    for i, word in enumerate(words):
        # First and last words are always capitalized
        if i == 0 or i == len(words) - 1:
            result.append(word.capitalize())
        # Check if word (lowercase) is in the list of words to keep lowercase
        elif word.lower() in lowercase_words:
            result.append(word.lower())
        else:
            result.append(word.capitalize())
    
    return ' '.join(result)

for line in sys.stdin:
    line = line.rstrip('\n')
    print(to_title_case(line))