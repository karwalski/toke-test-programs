import json
import sys
import csv
import io

def main():
    table_state = {}
    
    # Process each line from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        event = json.loads(line)
        op = event["op"]
        key = event["key"]
        
        if op == "I":  # INSERT
            table_state[key] = event["data"]
        elif op == "U":  # UPDATE
            table_state[key] = event["data"]
        elif op == "D":  # DELETE
            if key in table_state:
                del table_state[key]
    
    # Output as CSV
    if table_state:
        # Get column names from first record
        first_record = next(iter(table_state.values()))
        columns = sorted(first_record.keys())
        
        # Sort rows by key
        sorted_keys = sorted(table_state.keys())
        
        # Create CSV output
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(columns)
        
        # Write data rows
        for key in sorted_keys:
            row_data = table_state[key]
            row = [row_data[col] for col in columns]
            writer.writerow(row)
        
        # Print without trailing newline
        result = output.getvalue().rstrip('\n')
        print(result)

if __name__ == "__main__":
    main()