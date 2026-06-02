import json
import sys
import heapq

def main():
    input_data = sys.stdin.read().strip()
    operations = json.loads(input_data)
    
    # Using a max heap by negating priorities
    priority_queue = []
    
    for op in operations:
        if op["op"] == "enqueue":
            msg = op["msg"]
            priority = op["priority"]
            # Use negative priority for max heap behavior
            heapq.heappush(priority_queue, (-priority, msg))
        
        elif op["op"] == "dequeue":
            if priority_queue:
                neg_priority, msg = heapq.heappop(priority_queue)
                priority = -neg_priority
                print(f"dequeue: {msg} (priority {priority})")
            else:
                print("EMPTY")

if __name__ == "__main__":
    main()