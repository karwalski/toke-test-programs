import sys

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
    
    def find_completions(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        completions = []
        self._dfs(node, prefix, completions)
        return sorted(completions)[:5]
    
    def _dfs(self, node, current_word, completions):
        if node.is_word:
            completions.append(current_word)
        
        for char, child_node in node.children.items():
            self._dfs(child_node, current_word + char, completions)

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Find the blank line
blank_index = lines.index('')

# Build trie with words
trie = Trie()
for i in range(blank_index):
    if lines[i]:
        trie.insert(lines[i])

# Process queries
for i in range(blank_index + 1, len(lines)):
    prefix = lines[i]
    completions = trie.find_completions(prefix)
    print(f"{prefix}: {', '.join(completions)}")