import json
import sys

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the sections
    first_blank = -1
    second_blank = -1
    
    for i, line in enumerate(lines):
        if line == '':
            if first_blank == -1:
                first_blank = i
            else:
                second_blank = i
                break
    
    # Parse datasets
    dataset_a = []
    for i in range(first_blank):
        if lines[i].strip():
            dataset_a.append(json.loads(lines[i]))
    
    dataset_b = []
    for i in range(first_blank + 1, second_blank):
        if lines[i].strip():
            dataset_b.append(json.loads(lines[i]))
    
    # Get merge key
    merge_key = lines[second_blank + 1]
    
    # Create lookup for dataset A
    records = {}
    for record in dataset_a:
        key_val = record[merge_key]
        records[key_val] = record
    
    # Merge dataset B (last-write-wins)
    for record in dataset_b:
        key_val = record[merge_key]
        if key_val in records:
            # Merge fields, B wins conflicts
            merged = records[key_val].copy()
            merged.update(record)
            records[key_val] = merged
        else:
            records[key_val] = record
    
    # Output merged records sorted by key
    for key_val in sorted(records.keys()):
        print(json.dumps(records[key_val], separators=(',', ':')))

if __name__ == "__main__":
    main()