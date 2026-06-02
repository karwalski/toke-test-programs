import json
import sys
import random

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    students = input_data["students"]
    prompt = input_data["prompt"]
    seed = input_data["seed"]
    
    # Set random seed for reproducible results
    random.seed(seed)
    
    # Shuffle students to create random pairs
    shuffled_students = students.copy()
    random.shuffle(shuffled_students)
    
    # Create pairs
    pairs = []
    for i in range(0, len(shuffled_students), 2):
        if i + 1 < len(shuffled_students):
            pairs.append((shuffled_students[i], shuffled_students[i + 1]))
        else:
            # Handle odd number of students by putting last student with previous pair
            if pairs:
                last_pair = pairs[-1]
                pairs[-1] = (last_pair[0], last_pair[1])
    
    # Create share order (reverse order of pairs)
    share_order = pairs[::-1]
    
    # Output
    print(f"Prompt: {prompt}")
    print("Pairs:")
    for pair in pairs:
        print(f"  {pair[0]} & {pair[1]}")
    
    share_order_str = ", ".join([f"{pair[0]} & {pair[1]}" for pair in share_order])
    print(f"Share order: {share_order_str}")

if __name__ == "__main__":
    main()