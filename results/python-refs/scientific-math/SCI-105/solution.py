import sys

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    def _find_prefix_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def prefix_count(self, prefix):
        node = self._find_prefix_node(prefix)
        if node is None:
            return 0
        return self._count_words(node)
    
    def _count_words(self, node):
        count = 0
        if node.is_end_of_word:
            count = 1
        for child in node.children.values():
            count += self._count_words(child)
        return count
    
    def words_with_prefix(self, prefix):
        node = self._find_prefix_node(prefix)
        if node is None:
            return []
        words = []
        self._collect_words(node, prefix, words)
        return sorted(words)
    
    def _collect_words(self, node, current_word, words):
        if node.is_end_of_word:
            words.append(current_word)
        for char, child in node.children.items():
            self._collect_words(child, current_word + char, words)

trie = Trie()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split(' ', 1)
    command = parts[0]
    
    if command == "INSERT":
        word = parts[1]
        trie.insert(word)
    elif command == "SEARCH":
        word = parts[1]
        result = trie.search(word)
        print("true" if result else "false")
    elif command == "PREFIX":
        prefix = parts[1]
        count = trie.prefix_count(prefix)
        print(count)
    elif command == "WORDS_WITH":
        prefix = parts[1]
        words = trie.words_with_prefix(prefix)
        print(" ".join(words))