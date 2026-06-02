import time
import json
import sys

def main():
    # Read input
    port = int(input().strip())
    num_items = int(input().strip())
    
    # Print listening message
    print(f"Listening on :{port}")
    
    # Simulate streaming NDJSON with 10ms delay between items
    for i in range(num_items):
        # Create a JSON object for this item
        json_obj = {
            "id": i + 1,
            "data": f"item_{i + 1}",
            "timestamp": time.time()
        }
        
        # Print as NDJSON (one JSON object per line)
        print(json.dumps(json_obj))
        
        # 10ms delay between items
        time.sleep(0.01)

if __name__ == "__main__":
    main()