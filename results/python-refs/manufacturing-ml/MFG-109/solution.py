import csv
import json
import sys

def process_inspection_results():
    reader = csv.DictReader(sys.stdin)
    lots = []
    
    for row in reader:
        lot_id = row['lot_id']
        defects_found = int(row['defects_found'])
        accept_number = int(row['accept_number'])
        
        disposition = "accept" if defects_found <= accept_number else "reject"
        
        lots.append({
            "lot_id": lot_id,
            "disposition": disposition
        })
    
    result = {"lots": lots}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    process_inspection_results()