import csv
import json
import sys
import math

def calculate_kanban_cards(demand_rate, lead_time, safety_factor, container_size):
    # Kanban formula: (Demand Rate × Lead Time × (1 + Safety Factor)) / Container Size
    kanban_quantity = (demand_rate * lead_time * (1 + safety_factor)) / container_size
    return math.ceil(kanban_quantity)

def main():
    reader = csv.DictReader(sys.stdin)
    parts = []
    
    for row in reader:
        part = row['part']
        demand_rate = float(row['demand_rate'])
        lead_time = float(row['lead_time'])
        safety_factor = float(row['safety_factor'])
        container_size = float(row['container_size'])
        
        kanban_cards = calculate_kanban_cards(demand_rate, lead_time, safety_factor, container_size)
        
        parts.append({
            "part": part,
            "kanban_cards": kanban_cards
        })
    
    result = {"parts": parts}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()