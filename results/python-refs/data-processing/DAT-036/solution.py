import sys
import csv
from io import StringIO

def parse_input():
    content = sys.stdin.read().strip()
    sections = content.split('\n\n')
    
    base_csv = sections[0]
    version_a_csv = sections[1]
    version_b_csv = sections[2]
    key_column = sections[3]
    
    return base_csv, version_a_csv, version_b_csv, key_column

def csv_to_dict(csv_text):
    reader = csv.DictReader(StringIO(csv_text))
    return {row[list(row.keys())[0]]: row for row in reader}

def dict_to_csv(data_dict, fieldnames):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in data_dict.values():
        writer.writerow(row)
    return output.getvalue().strip()

def three_way_merge(base_dict, version_a_dict, version_b_dict, key_column):
    merged = {}
    all_keys = set(base_dict.keys()) | set(version_a_dict.keys()) | set(version_b_dict.keys())
    
    for key in all_keys:
        base_row = base_dict.get(key, {})
        a_row = version_a_dict.get(key, {})
        b_row = version_b_dict.get(key, {})
        
        # Start with base row or empty dict
        merged_row = base_row.copy() if base_row else {}
        
        # Get all possible fields
        all_fields = set()
        if base_row:
            all_fields.update(base_row.keys())
        if a_row:
            all_fields.update(a_row.keys())
        if b_row:
            all_fields.update(b_row.keys())
        
        for field in all_fields:
            base_val = base_row.get(field, '')
            a_val = a_row.get(field, '')
            b_val = b_row.get(field, '')
            
            # If both versions changed the field differently from base
            if (a_val != base_val and b_val != base_val and a_val != b_val):
                merged_row[field] = f"CONFLICT({a_val},{b_val})"
            # If only A changed
            elif a_val != base_val and b_val == base_val:
                merged_row[field] = a_val
            # If only B changed
            elif b_val != base_val and a_val == base_val:
                merged_row[field] = b_val
            # If both changed to the same value or no change
            elif a_val == b_val:
                merged_row[field] = a_val if a_val else base_val
            else:
                merged_row[field] = base_val
        
        merged[key] = merged_row
    
    return merged

def main():
    base_csv, version_a_csv, version_b_csv, key_column = parse_input()
    
    base_dict = csv_to_dict(base_csv)
    version_a_dict = csv_to_dict(version_a_csv)
    version_b_dict = csv_to_dict(version_b_csv)
    
    # Get fieldnames from any non-empty dataset
    fieldnames = None
    if base_dict:
        fieldnames = list(next(iter(base_dict.values())).keys())
    elif version_a_dict:
        fieldnames = list(next(iter(version_a_dict.values())).keys())
    elif version_b_dict:
        fieldnames = list(next(iter(version_b_dict.values())).keys())
    
    merged_dict = three_way_merge(base_dict, version_a_dict, version_b_dict, key_column)
    
    result = dict_to_csv(merged_dict, fieldnames)
    print(result)

if __name__ == "__main__":
    main()