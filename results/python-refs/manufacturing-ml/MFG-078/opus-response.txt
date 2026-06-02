import sys
import csv
import json
import math

def main():
    csv_reader = csv.DictReader(sys.stdin)
    features = []
    for row in csv_reader:
        nominal_x = float(row['nominal_x'])
        nominal_y = float(row['nominal_y'])
        actual_x = float(row['actual_x'])
        actual_y = float(row['actual_y'])
        tolerance = float(row['tolerance'])
        dx = actual_x - nominal_x
        dy = actual_y - nominal_y
        true_position = round(2 * math.sqrt(dx**2 + dy**2), 2)
        features.append({
            "true_position": true_position,
            "tolerance": tolerance,
            "pass": true_position <= tolerance
        })
    print(json.dumps({"features": features}, separators=(',', ':')))

if __name__ == "__main__":
    main()