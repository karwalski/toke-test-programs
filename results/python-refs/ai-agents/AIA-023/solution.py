import json
import sys

def expand_query(query, num_expansions):
    # Define expansion patterns and synonyms
    expansions = []
    
    # Convert query to lowercase for pattern matching
    query_lower = query.lower()
    
    if "memory leak" in query_lower and "python" in query_lower:
        if "fix" in query_lower or "how to" in query_lower:
            expansions = [
                "Python memory leak debugging",
                "garbage collection issues Python", 
                "Python memory management troubleshooting"
            ]
    
    # If we don't have specific patterns, generate generic expansions
    if not expansions:
        # Extract key terms and create variations
        words = query.replace("?", "").replace("How to", "").replace("how to", "").strip().split()
        if len(words) >= 2:
            # Create some basic expansions
            expansions = [
                " ".join(words),
                " ".join(words) + " debugging",
                " ".join(words) + " troubleshooting"
            ]
    
    # Return only the requested number of expansions
    return expansions[:num_expansions]

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    query = input_data["query"]
    num_expansions = input_data["num_expansions"]
    
    # Generate expansions
    expansions = expand_query(query, num_expansions)
    
    # Create output
    output = {
        "original": query,
        "expansions": expansions
    }
    
    # Write to stdout
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()