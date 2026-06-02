import sys
import random

def build_markov_chain(text):
    words = text.split()
    chain = {}
    
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        
        if current_word not in chain:
            chain[current_word] = []
        chain[current_word].append(next_word)
    
    return chain

def generate_text(chain, seed, count):
    random.seed(seed)
    result = []
    current_word = None
    
    # Find a starting word that exists in the chain
    words_in_chain = list(chain.keys())
    if words_in_chain:
        current_word = random.choice(words_in_chain)
    
    for _ in range(count):
        if current_word is None or current_word not in chain:
            break
        
        result.append(current_word)
        next_words = chain[current_word]
        current_word = random.choice(next_words)
    
    return ' '.join(result)

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Find the blank line
blank_line_index = -1
for i, line in enumerate(lines):
    if line == '':
        blank_line_index = i
        break

# Extract training text
training_text = ' '.join(lines[:blank_line_index])

# Extract parameters
params = lines[blank_line_index + 1].split()
count = int(params[0])
seed = int(params[1])

# Build chain and generate text
chain = build_markov_chain(training_text)
output = generate_text(chain, seed, count)
print(output)