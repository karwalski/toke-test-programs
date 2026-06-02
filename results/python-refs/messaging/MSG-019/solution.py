import json
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    operations = json.loads(input_data)
    
    # Dictionary to store topic subscriptions
    # topic -> set of clients
    subscriptions = {}
    
    # Process each operation
    for op in operations:
        if op["op"] == "subscribe":
            client = op["client"]
            topic = op["topic"]
            
            if topic not in subscriptions:
                subscriptions[topic] = set()
            subscriptions[topic].add(client)
            
        elif op["op"] == "unsubscribe":
            client = op["client"]
            topic = op["topic"]
            
            if topic in subscriptions:
                subscriptions[topic].discard(client)
                
        elif op["op"] == "publish":
            topic = op["topic"]
            message = op["message"]
            
            # Get subscribers for this topic
            subscribers = subscriptions.get(topic, set())
            
            # Sort subscribers for consistent output
            sorted_subscribers = sorted(subscribers)
            
            # Format output
            subscribers_str = ", ".join(sorted_subscribers)
            print(f'publish {topic} "{message}": {subscribers_str}')

if __name__ == "__main__":
    main()