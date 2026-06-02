import sys
import csv
from io import StringIO

def main():
    # Read all input
    input_text = sys.stdin.read().strip()
    
    # Split by section markers
    sections = input_text.split('\n---\n')
    
    # Parse each section as CSV
    all_data = []
    all_columns = set()
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        # Parse CSV section
        csv_reader = csv.reader(StringIO(section))
        rows = list(csv_reader)
        
        if rows:
            headers = rows[0]
            all_columns.update(headers)
            
            # Store data with section info
            for row in rows[1:]:
                row_dict = {}
                for i, value in enumerate(row):
                    if i < len(headers):
                        row_dict[headers[i]] = value
                all_data.append(row_dict)
    
    # Sort columns alphabetically
    sorted_columns = sorted(all_columns)
    
    # Output CSV
    csv_writer = csv.writer(sys.stdout)
    
    # Write header
    csv_writer.writerow(sorted_columns)
    
    # Write data rows
    for row_dict in all_data:
        row = []
        for col in sorted_columns:
            row.append(row_dict.get(col, ''))
        csv_writer.writerow(row)

if __name__ == '__main__':
    main()