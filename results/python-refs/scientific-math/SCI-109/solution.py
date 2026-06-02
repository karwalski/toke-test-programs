import random
import sys

class SkipListNode:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.header = SkipListNode(float('-inf'), max_level)
        self.level = 0
    
    def random_level(self):
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level
    
    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        return current and current.key == key
    
    def insert(self, key):
        update = [None] * (self.max_level + 1)
        current = self.header
        
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        
        if current and current.key == key:
            return
        
        new_level = self.random_level()
        
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level
        
        new_node = SkipListNode(key, new_level)
        
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
    
    def delete(self, key):
        update = [None] * (self.max_level + 1)
        current = self.header
        
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        
        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]
            
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
    
    def range_query(self, lo, hi):
        result = []
        current = self.header
        
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < lo:
                current = current.forward[i]
        
        current = current.forward[0]
        
        while current and current.key <= hi:
            result.append(current.key)
            current = current.forward[0]
        
        return result
    
    def print_list(self):
        for level in range(self.level, -1, -1):
            nodes = []
            current = self.header.forward[level]
            while current:
                nodes.append(str(current.key))
                current = current.forward[level]
            if nodes:
                print(' '.join(nodes))

skip_list = SkipList()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    command = parts[0]
    
    if command == "INSERT":
        key = int(parts[1])
        skip_list.insert(key)
    
    elif command == "DELETE":
        key = int(parts[1])
        skip_list.delete(key)
    
    elif command == "SEARCH":
        key = int(parts[1])
        if skip_list.search(key):
            print(f"FOUND {key}")
        else:
            print("NOT FOUND")
    
    elif command == "RANGE":
        lo = int(parts[1])
        hi = int(parts[2])
        result = skip_list.range_query(lo, hi)
        print(' '.join(map(str, result)))
    
    elif command == "PRINT":
        skip_list.print_list()