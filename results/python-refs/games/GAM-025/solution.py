import json
import sys

def main():
    # Read input
    input_lines = []
    for line in sys.stdin:
        input_lines.append(line.rstrip('\n'))
    
    # Find the blank line that separates JSON from commands
    blank_line_index = -1
    for i, line in enumerate(input_lines):
        if line == "":
            blank_line_index = i
            break
    
    # Parse JSON map
    json_text = "\n".join(input_lines[:blank_line_index])
    map_data = json.loads(json_text)
    
    # Get commands
    commands = input_lines[blank_line_index + 1:] if blank_line_index != -1 else []
    
    # Initialize game state
    current_room = map_data["start"]
    rooms = map_data["rooms"]
    
    def show_room():
        room = rooms[current_room]
        print(room["desc"])
        exits = list(room["exits"].keys())
        print("Exits: " + ", ".join(exits))
    
    # Process commands
    for command in commands:
        command = command.strip().lower()
        
        if command == "look":
            show_room()
        elif command in rooms[current_room]["exits"]:
            # Move to new room
            current_room = rooms[current_room]["exits"][command]
            show_room()

if __name__ == "__main__":
    main()