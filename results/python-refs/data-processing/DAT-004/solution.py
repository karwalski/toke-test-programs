import sys
import json

def validate_json():
    try:
        # Read all input from stdin
        input_data = sys.stdin.read()
        
        # Try to parse the JSON
        json.loads(input_data)
        
        # If parsing succeeds, it's valid JSON
        print("Valid JSON")
        
    except json.JSONDecodeError as e:
        # Extract line and column information from the exception
        line_num = e.lineno
        col_num = e.colno
        description = e.msg
        
        # Format and print the error message
        print(f"Error at line {line_num} col {col_num}: {description}")

if __name__ == "__main__":
    validate_json()