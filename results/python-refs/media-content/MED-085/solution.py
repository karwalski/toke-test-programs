import sys
from difflib import SequenceMatcher

def word_diff(text1, text2):
    words1 = text1.split()
    words2 = text2.split()
    
    matcher = SequenceMatcher(None, words1, words2)
    result = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            result.extend(words1[i1:i2])
        elif tag == 'delete':
            for word in words1[i1:i2]:
                result.append(f'[-{word}-]')
        elif tag == 'insert':
            for word in words2[j1:j2]:
                result.append(f'{{+{word}+}}')
        elif tag == 'replace':
            for word in words1[i1:i2]:
                result.append(f'[-{word}-]')
            for word in words2[j1:j2]:
                result.append(f'{{+{word}+}}')
    
    return ' '.join(result)

# Read input
input_text = sys.stdin.read().strip()
lines = input_text.split('---')
text1 = lines[0].strip()
text2 = lines[1].strip()

# Generate and print diff
print(word_diff(text1, text2))