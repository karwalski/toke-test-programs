import hashlib
import sys

class PatriciaTrieNode:
    def __init__(self):
        self.children = {}
        self.value = None
        self.key = ""
        self.is_leaf = False

class PatriciaTrie:
    def __init__(self):
        self.root = PatriciaTrieNode()
    
    def insert(self, key, value):
        self._insert_recursive(self.root, key, value)
    
    def _insert_recursive(self, node, key, value):
        if not key:
            node.value = value
            node.is_leaf = True
            return
        
        # Find matching child
        for child_key, child_node in node.children.items():
            common_prefix = self._common_prefix(key, child_key)
            if common_prefix:
                if common_prefix == child_key:
                    # Continue down this path
                    remaining_key = key[len(common_prefix):]
                    self._insert_recursive(child_node, remaining_key, value)
                    return
                else:
                    # Split the edge
                    # Remove old child
                    del node.children[child_key]
                    
                    # Create intermediate node
                    intermediate = PatriciaTrieNode()
                    intermediate.key = common_prefix
                    
                    # Update old child
                    old_child_key = child_key[len(common_prefix):]
                    intermediate.children[old_child_key] = child_node
                    
                    # Add new path
                    remaining_key = key[len(common_prefix):]
                    if remaining_key:
                        new_child = PatriciaTrieNode()
                        new_child.key = remaining_key
                        new_child.value = value
                        new_child.is_leaf = True
                        intermediate.children[remaining_key] = new_child
                    else:
                        intermediate.value = value
                        intermediate.is_leaf = True
                    
                    node.children[common_prefix] = intermediate
                    return
        
        # No matching child found, create new one
        new_child = PatriciaTrieNode()
        new_child.key = key
        new_child.value = value
        new_child.is_leaf = True
        node.children[key] = new_child
    
    def _common_prefix(self, s1, s2):
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return s1[:i]
    
    def lookup(self, key):
        return self._lookup_recursive(self.root, key)
    
    def _lookup_recursive(self, node, key):
        if not key:
            return node.value if node.is_leaf else None
        
        for child_key, child_node in node.children.items():
            if key.startswith(child_key):
                remaining_key = key[len(child_key):]
                return self._lookup_recursive(child_node, remaining_key)
        
        return None
    
    def get_root_hash(self):
        return self._hash_node(self.root)
    
    def _hash_node(self, node):
        # Create a deterministic string representation of the node
        data = ""
        
        # Add value if present
        if node.is_leaf and node.value:
            data += f"value:{node.value}"
        
        # Add children in sorted order for determinism
        for child_key in sorted(node.children.keys()):
            child_hash = self._hash_node(node.children[child_key])
            data += f"child:{child_key}:{child_hash}"
        
        # Hash the data
        return hashlib.sha256(data.encode()).hexdigest()

def main():
    trie = PatriciaTrie()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split()
        command = parts[0]
        
        if command == "INSERT":
            key = parts[1]
            value = parts[2]
            trie.insert(key, value)
        
        elif command == "LOOKUP":
            key = parts[1]
            result = trie.lookup(key)
            if result is not None:
                print(result)
            else:
                print("NOT_FOUND")
        
        elif command == "ROOT":
            root_hash = trie.get_root_hash()
            print(root_hash)

if __name__ == "__main__":
    main()