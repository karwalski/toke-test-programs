import sys
import csv
from collections import Counter

def analyze_duplicates():
    # Read CSV from stdin
    reader = csv.reader(sys.stdin)
    rows = list(reader)
    
    if not rows:
        return
    
    headers = rows[0]
    data_rows = rows[1:]
    
    total_rows = len(data_rows)
    
    # Convert data rows to tuples for counting
    row_tuples = [tuple(row) for row in data_rows]
    row_counts = Counter(row_tuples)
    
    # Find exact duplicates (rows that appear more than once)
    duplicate_rows = {row: count for row, count in row_counts.items() if count > 1}
    exact_duplicates = sum(count - 1 for count in duplicate_rows.values())
    
    # Calculate column duplication percentages
    column_stats = {}
    for i, header in enumerate(headers):
        column_values = [row[i] for row in data_rows]
        value_counts = Counter(column_values)
        # Calculate percentage of duplicate values
        total_duplicates = sum(count - 1 for count in value_counts.values() if count > 1)
        duplicate_percentage = (total_duplicates + len(value_counts)) / total_rows * 100
        column_stats[header] = duplicate_percentage
    
    # Output the report
    print(f"Total rows: {total_rows}")
    print(f"Exact duplicates: {exact_duplicates}")
    
    if duplicate_rows:
        print("Duplicate rows:")
        for row, count in duplicate_rows.items():
            row_str = "(" + ",".join(row) + ")"
            print(f"  {row_str} x{count}")
    
    # Sort columns by header name for consistent output
    column_items = sorted(column_stats.items())
    column_output = ", ".join([f"{header} {percentage}%" for header, percentage in column_items])
    print(f"Column duplication: {column_output}")

if __name__ == "__main__":
    analyze_duplicates()