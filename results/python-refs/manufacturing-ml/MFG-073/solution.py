import csv
import json
import sys

def main():
    # Read CSV from stdin
    reader = csv.DictReader(sys.stdin)
    
    # Group data by material_lot
    lots = {}
    
    for row in reader:
        material_lot = row['material_lot']
        product_id = row['product_id']
        result = row['result']
        
        if material_lot not in lots:
            lots[material_lot] = {
                'products': [],
                'total_count': 0,
                'pass_count': 0
            }
        
        lots[material_lot]['products'].append(product_id)
        lots[material_lot]['total_count'] += 1
        
        if result == 'pass':
            lots[material_lot]['pass_count'] += 1
    
    # Calculate pass rates and format output
    output_lots = {}
    for lot_id, data in lots.items():
        pass_rate = data['pass_count'] / data['total_count'] if data['total_count'] > 0 else 0.0
        output_lots[lot_id] = {
            'products': data['products'],
            'pass_rate': pass_rate
        }
    
    # Create final output structure
    result = {'lots': output_lots}
    
    # Output JSON without extra whitespace
    print(json.dumps(result, separators=(',', ':')))

if __name__ == '__main__':
    main()