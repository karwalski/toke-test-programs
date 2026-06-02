import json
import sys

def calculate_sm2_interval(ease, interval, grade):
    if grade < 3:
        return 1
    elif interval == 1:
        return 6
    elif interval == 6:
        return int(interval * ease)
    else:
        return int(interval * ease)

def main():
    # Read JSON input
    json_input = input().strip()
    cards = json.loads(json_input)
    
    for card in cards:
        # Show front of card
        print(f"Q: {card['front']}")
        
        # Show back of card
        print(f"A: {card['back']}")
        
        # Get grade
        grade = int(input())
        
        # Calculate new interval
        new_interval = calculate_sm2_interval(card['ease'], card['interval'], grade)
        
        # Show result
        print(f"Grade: {grade} | New interval: {new_interval} days")
    
    print("Session complete.")

if __name__ == "__main__":
    main()