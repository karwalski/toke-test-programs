import sys
import csv
from io import StringIO

def main():
    # Read all input from stdin
    input_data = sys.stdin.read()
    
    # Parse CSV data
    csv_reader = csv.reader(StringIO(input_data))
    rows = list(csv_reader)
    
    if not rows:
        return
    
    headers = rows[0]
    data_rows = rows[1:]
    
    if not data_rows:
        return
    
    total_rows = len(data_rows)
    column_scores = []
    
    for col_idx, column_name in enumerate(headers):
        # Get all values for this column
        column_values = [row[col_idx] if col_idx < len(row) else '' for row in data_rows]
        
        # Calculate completeness (non-empty values)
        non_empty_count = sum(1 for value in column_values if value.strip() != '')
        completeness = (non_empty_count / total_rows) * 100
        
        # Calculate uniqueness (unique values among non-empty values)
        non_empty_values = [value for value in column_values if value.strip() != '']
        if non_empty_values:
            unique_values = len(set(non_empty_values))
            uniqueness = (unique_values / len(non_empty_values)) * 100
        else:
            uniqueness = 100.0
        
        # Output column report
        print(f"Column: {column_name}")
        print(f"  Completeness: {completeness:.1f}%")
        print(f"  Uniqueness: {uniqueness:.1f}%")
        
        # Store average score for this column
        column_score = (completeness + uniqueness) / 2
        column_scores.append(column_score)
    
    # Calculate overall score
    overall_score = sum(column_scores) / len(column_scores)
    print(f"Overall score: {overall_score:.1f}%")

if __name__ == "__main__":
    main()