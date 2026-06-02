import sys

# Read input
lines = sys.stdin.read().strip().split('\n')
first_line = lines[0].split()
word = first_line[0]
n = int(first_line[1])

# Join all text lines
text = ' '.join(lines[1:])

# Split text into words
words = text.split()

# Find all occurrences of the word
for i, w in enumerate(words):
    if w.lower() == word.lower():
        # Get context around the word
        start = max(0, i - n)
        end = min(len(words), i + n + 1)
        
        # Build context
        context_words = words[start:end]
        
        # Replace the target word with [WORD] (case preserved from search term)
        for j in range(len(context_words)):
            if context_words[j].lower() == word.lower():
                context_words[j] = f'[{word}]'
                break
        
        # Build output line
        context_text = ' '.join(context_words)
        
        # Add ellipsis if needed
        if start > 0:
            context_text = '...' + context_text
        if end < len(words):
            context_text = context_text + '...'
        else:
            context_text = context_text + ' <END>'
        
        print(context_text)