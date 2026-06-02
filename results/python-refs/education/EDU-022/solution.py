import json
import sys
from datetime import datetime, timedelta

def main():
    # Read JSON input from stdin
    input_data = sys.stdin.read().strip()
    cards = json.loads(input_data)
    
    # Calculate due dates for each card
    results = []
    for card in cards:
        card_id = card["card_id"]
        last_reviewed = datetime.strptime(card["last_reviewed"], "%Y-%m-%d")
        interval_days = card["interval_days"]
        
        # Calculate due date by adding interval to last reviewed date
        due_date = last_reviewed + timedelta(days=interval_days)
        due_date_str = due_date.strftime("%Y-%m-%d")
        
        results.append((due_date, f"{card_id}: due {due_date_str} (interval {interval_days} days)"))
    
    # Sort by due date
    results.sort(key=lambda x: x[0])
    
    # Output results
    for _, output_line in results:
        print(output_line)

if __name__ == "__main__":
    main()