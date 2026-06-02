import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract the operations array
    operations = input_data.get("operations", [])
    
    # Process each operation
    results = []
    succeeded = 0
    failed = 0
    
    for index, operation in enumerate(operations):
        action = operation.get("action")
        
        # Simulate API operation responses
        if action == "like_post":
            result = {
                "index": index,
                "status": "success",
                "data": {"liked": True}
            }
            succeeded += 1
        elif action == "follow":
            result = {
                "index": index,
                "status": "success", 
                "data": {"following": True}
            }
            succeeded += 1
        else:
            result = {
                "index": index,
                "status": "error",
                "data": {"message": "Unknown action"}
            }
            failed += 1
            
        results.append(result)
    
    # Create response
    response = {
        "results": results,
        "total": len(operations),
        "succeeded": succeeded,
        "failed": failed
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()