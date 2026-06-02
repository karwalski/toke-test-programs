import heapq
import sys

class MinHeapPriorityQueue:
    def __init__(self):
        self.heap = []
        self.key_to_index = {}
        self.deleted = set()
        self.counter = 0
    
    def insert(self, key, value):
        entry = [key, self.counter, value, False]
        self.key_to_index[key] = entry
        heapq.heappush(self.heap, entry)
        self.counter += 1
    
    def extract_min(self):
        while self.heap:
            key, count, value, deleted = heapq.heappop(self.heap)
            if not deleted:
                del self.key_to_index[key]
                return key, value
        return None
    
    def peek(self):
        while self.heap:
            key, count, value, deleted = self.heap[0]
            if not deleted:
                return key, value
            heapq.heappop(self.heap)
        return None
    
    def decrease_key(self, key, new_value):
        if key in self.key_to_index:
            old_entry = self.key_to_index[key]
            old_entry[3] = True  # Mark as deleted
            self.insert(key, new_value)
    
    def delete(self, key):
        if key in self.key_to_index:
            entry = self.key_to_index[key]
            entry[3] = True  # Mark as deleted
            del self.key_to_index[key]
    
    def size(self):
        return len(self.key_to_index)

pq = MinHeapPriorityQueue()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    command = parts[0]
    
    if command == "INSERT":
        key = int(parts[1])
        value = parts[2]
        pq.insert(key, value)
    
    elif command == "EXTRACT_MIN":
        result = pq.extract_min()
        if result:
            key, value = result
            print(f"key={key} value={value}")
    
    elif command == "PEEK":
        result = pq.peek()
        if result:
            key, value = result
            print(f"key={key} value={value}")
    
    elif command == "DECREASE_KEY":
        key = int(parts[1])
        new_value = parts[2]
        pq.decrease_key(key, new_value)
    
    elif command == "DELETE":
        key = int(parts[1])
        pq.delete(key)
    
    elif command == "SIZE":
        print(pq.size())