import sys

class SuffixTreeNode:
    def __init__(self):
        self.children = {}
        self.start = -1
        self.end = [-1]
        self.suffix_link = None
        self.suffix_index = -1

class SuffixTree:
    def __init__(self, text):
        self.text = text + '$'
        self.n = len(self.text)
        self.root = SuffixTreeNode()
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remaining_suffix_count = 0
        self.leaf_end = [-1]
        self.root_end = None
        self.split_end = [-1]
        self.size = -1
        
        self.build_suffix_tree()
    
    def edge_length(self, node):
        if node == self.root:
            return 0
        return node.end[0] - node.start + 1
    
    def walk_down(self, curr_node):
        if self.active_length >= self.edge_length(curr_node):
            self.active_edge += self.edge_length(curr_node)
            self.active_length -= self.edge_length(curr_node)
            self.active_node = curr_node
            return True
        return False
    
    def new_node(self, start, end=None):
        node = SuffixTreeNode()
        node.suffix_link = self.root
        node.start = start
        if end is None:
            node.end = self.leaf_end
        else:
            node.end = end
        node.suffix_index = -1
        return node
    
    def extend_suffix_tree(self, pos):
        self.leaf_end[0] = pos
        self.remaining_suffix_count += 1
        last_new_node = None
        
        while self.remaining_suffix_count > 0:
            if self.active_length == 0:
                self.active_edge = pos
            
            if self.text[self.active_edge] not in self.active_node.children:
                leaf = self.new_node(pos)
                self.active_node.children[self.text[self.active_edge]] = leaf
                
                if last_new_node is not None:
                    last_new_node.suffix_link = self.active_node
                    last_new_node = None
            else:
                next_node = self.active_node.children[self.text[self.active_edge]]
                if self.walk_down(next_node):
                    continue
                
                if self.text[next_node.start + self.active_length] == self.text[pos]:
                    if last_new_node is not None and self.active_node != self.root:
                        last_new_node.suffix_link = self.active_node
                        last_new_node = None
                    self.active_length += 1
                    break
                
                self.split_end[0] = next_node.start + self.active_length - 1
                split = self.new_node(next_node.start, self.split_end)
                self.active_node.children[self.text[self.active_edge]] = split
                
                leaf = self.new_node(pos)
                split.children[self.text[pos]] = leaf
                next_node.start += self.active_length
                split.children[self.text[next_node.start]] = next_node
                
                if last_new_node is not None:
                    last_new_node.suffix_link = split
                
                last_new_node = split
            
            self.remaining_suffix_count -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remaining_suffix_count + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link
    
    def build_suffix_tree(self):
        self.size = len(self.text)
        self.root_end = [-1]
        self.root.end = self.root_end
        
        for i in range(self.size):
            self.extend_suffix_tree(i)
    
    def search_pattern(self, pattern):
        node = self.root
        i = 0
        
        while i < len(pattern):
            if pattern[i] in node.children:
                child = node.children[pattern[i]]
                edge_start = child.start
                edge_end = child.end[0]
                
                j = edge_start
                while j <= edge_end and i < len(pattern):
                    if self.text[j] != pattern[i]:
                        return False, 0
                    i += 1
                    j += 1
                
                if i < len(pattern):
                    node = child
            else:
                return False, 0
        
        return True, self.count_leaves(node if i >= len(pattern) else child)
    
    def count_leaves(self, node):
        if not node.children:
            return 1
        
        count = 0
        for child in node.children.values():
            count += self.count_leaves(child)
        return count
    
    def find_longest_repeated_substring(self):
        max_length = 0
        lrs = ""
        
        def dfs(node, depth, path):
            nonlocal max_length, lrs
            
            if not node.children:
                return
            
            if len(node.children) > 1 or node != self.root:
                if depth > max_length and node != self.root:
                    max_length = depth
                    lrs = path
            
            for char, child in node.children.items():
                if char != '$':
                    edge_length = child.end[0] - child.start + 1
                    edge_str = self.text[child.start:child.start + edge_length]
                    if '$' in edge_str:
                        edge_str = edge_str[:edge_str.index('$')]
                    
                    if edge_str:
                        dfs(child, depth + len(edge_str), path + edge_str)
        
        dfs(self.root, 0, "")
        return lrs

# Main program
text = input().strip()
suffix_tree = SuffixTree(text)

while True:
    try:
        line = input().strip()
        if not line:
            break
        
        if line.startswith("SEARCH "):
            pattern = line[7:]
            found, count = suffix_tree.search_pattern(pattern)
            if found:
                print(f"FOUND {count}")
            else:
                print("NOT FOUND")
        
        elif line.startswith("COUNT "):
            pattern = line[6:]
            found, count = suffix_tree.search_pattern(pattern)
            print(count)
        
        elif line == "LRS":
            lrs = suffix_tree.find_longest_repeated_substring()
            print(lrs)
    
    except EOFError:
        break