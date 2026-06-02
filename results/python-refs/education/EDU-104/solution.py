import json
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    responses = json.loads(input_data)
    
    # Initialize counters
    counts = {"V": 0, "A": 0, "R": 0, "K": 0}
    
    # Count responses
    for response in responses:
        answer = response["answer"]
        if answer in counts:
            counts[answer] += 1
    
    # Find dominant style
    max_count = max(counts.values())
    dominant_key = None
    for key, count in counts.items():
        if count == max_count:
            dominant_key = key
            break
    
    # Map to full names and descriptions
    style_names = {
        "V": "Visual",
        "A": "Aural", 
        "R": "Read/Write",
        "K": "Kinesthetic"
    }
    
    descriptions = {
        "Visual": "You learn best through diagrams, charts, and visual representations.",
        "Aural": "You learn best through listening, discussion, and verbal instruction.",
        "Read/Write": "You learn best through reading text and writing notes.",
        "Kinesthetic": "You learn best through hands-on experience and physical activity."
    }
    
    # Output results
    print(f"Visual: {counts['V']}")
    print(f"Aural: {counts['A']}")
    print(f"Read/Write: {counts['R']}")
    print(f"Kinesthetic: {counts['K']}")
    print(f"Dominant style: {style_names[dominant_key]}")
    print(descriptions[style_names[dominant_key]])

if __name__ == "__main__":
    main()