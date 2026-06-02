import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    students = input_data["students"]
    prompt = input_data["prompt"]
    
    pairs = []
    i = 0
    while i < len(students):
        if i + 1 < len(students):
            pairs.append((students[i], students[i+1]))
            i += 2
        else:
            pairs.append((students[i],))
            i += 1
    
    print(f"Prompt: {prompt}")
    print("Pairs:")
    for pair in pairs:
        if len(pair) == 2:
            print(f"  {pair[0]} & {pair[1]}")
        else:
            print(f"  {pair[0]} (solo)")
    
    share_order = pairs[::-1]
    parts = []
    for pair in share_order:
        if len(pair) == 2:
            parts.append(f"{pair[0]} & {pair[1]}")
        else:
            parts.append(f"{pair[0]}")
    print(f"Share order: {', '.join(parts)}")

if __name__ == "__main__":
    main()