import json
import sys

class PersistentMessageQueue:
    def __init__(self):
        self.queue = []
        self.unacked = []
        
    def enqueue(self, msg):
        self.queue.append(msg)
        return f"enqueue {msg}: ok (size={len(self.queue)})"
    
    def dequeue(self):
        if not self.queue:
            return "dequeue: empty"
        msg = self.queue.pop(0)
        self.unacked.append(msg)
        return f"dequeue: {msg} (unacked)"
    
    def peek(self):
        if not self.queue:
            return "peek: empty"
        return f"peek: {self.queue[0]}"
    
    def ack(self, msg):
        if msg in self.unacked:
            self.unacked.remove(msg)
            return f"ack {msg}: ok"
        return f"ack {msg}: not found"
    
    def crash(self):
        # On crash, unacked messages are lost from memory but should be recoverable
        return "crash: lost in-flight messages"
    
    def recover(self):
        # On recover, unacked messages are re-queued at the front
        requeued_count = len(self.unacked)
        # Add unacked messages back to the front of the queue
        self.queue = self.unacked + self.queue
        self.unacked = []
        return f"recover: requeued {requeued_count} unacked"

def main():
    input_data = sys.stdin.read().strip()
    operations = json.loads(input_data)
    
    mq = PersistentMessageQueue()
    
    for op in operations:
        operation = op["op"]
        
        if operation == "enqueue":
            result = mq.enqueue(op["msg"])
        elif operation == "dequeue":
            result = mq.dequeue()
        elif operation == "peek":
            result = mq.peek()
        elif operation == "ack":
            result = mq.ack(op["msg"])
        elif operation == "crash":
            result = mq.crash()
        elif operation == "recover":
            result = mq.recover()
        
        print(result)

if __name__ == "__main__":
    main()