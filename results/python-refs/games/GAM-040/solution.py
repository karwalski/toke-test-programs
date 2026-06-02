from collections import deque

def get_neighbors(word, word_set):
    neighbors = []
    for i in range(len(word)):
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if c != word[i]:
                new_word = word[:i] + c + word[i+1:]
                if new_word in word_set:
                    neighbors.append(new_word)
    return neighbors

def find_word_ladder(start, end, dictionary):
    if start == end:
        return [start]
    
    word_set = set(dictionary)
    if end not in word_set:
        return None
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current_word, path = queue.popleft()
        
        for neighbor in get_neighbors(current_word, word_set):
            if neighbor == end:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None

# Read input
start = input().strip()
end = input().strip()
dictionary = []
try:
    while True:
        word = input().strip()
        dictionary.append(word)
except EOFError:
    pass

# Find and print result
result = find_word_ladder(start, end, dictionary)
if result:
    print(' '.join(result))
else:
    print('No ladder')