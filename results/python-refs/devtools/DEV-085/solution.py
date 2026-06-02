import json
import sys

def main():
    # Read JSON from stdin
    input_data = sys.stdin.read().strip()
    comments = json.loads(input_data)
    
    # Define severity order for sorting
    severity_order = {"error": 0, "warning": 1, "info": 2}
    
    # Sort by file, then severity, then line
    comments.sort(key=lambda x: (x["file"], severity_order.get(x["severity"].lower(), 999), x["line"]))
    
    # Format and output each comment
    for comment in comments:
        severity_upper = comment["severity"].upper()
        print(f"{comment['file']}:{comment['line']} [{severity_upper}] {comment['message']}")

if __name__ == "__main__":
    main()