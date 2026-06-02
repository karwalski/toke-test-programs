import sys
import csv
from collections import Counter

def analyze_duplicates():
    reader = csv.reader(sys.stdin)
    rows = list(reader)
    
    if not rows:
        return
    
    headers = rows[0]
    data_rows = rows[1:]
    
    total_rows = len(data_rows)
    
    row_tuples = [tuple(row) for row in data_rows]
    row_counts = Counter(row_tuples)
    
    duplicate_rows = {row: count for row, count in row_counts.items() if count > 1}
    exact_duplicates = sum(count - 1 for count in duplicate_rows.values())
    
    print(f"Total rows: {total_rows}")
    print(f"Exact duplicates: {exact_duplicates}")
    
    if not duplicate_rows:
        print("No duplicates found")
        return
    
    print("Duplicate rows:")
    sorted_dups = sorted(duplicate_rows.items(), key=lambda x: -x[1])
    for row, count in sorted_dups:
        row_str = "(" + ",".join(row) + ")"
        print(f"  {row_str} x{count}")
    
    # Column duplication: percentage of rows whose value appears more than once
    column_stats = []
    for i, header in enumerate(headers):
        column_values = [row[i] for row in data_rows]
        value_counts = Counter(column_values)
        dup_count = sum(c for c in value_counts.values() if c > 1)
        pct = dup_count / total_rows * 100
        column_stats.append((header, pct))
    
    column_stats.sort(key=lambda x: -x[1])
    column_output = ", ".join([f"{h} {p}%" for h, p in column_stats])
    print(f"Column duplication: {column_output}")

if __name__ == "__main__":
    analyze_duplicates()