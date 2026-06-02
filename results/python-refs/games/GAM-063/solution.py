import sys

# Read initial time
initial_time = int(input())

# Initialize player times
white_time = initial_time
black_time = initial_time

# Track whose turn it is (True for White, False for Black)
white_turn = True

# Read move times until EOF
try:
    while True:
        move_time = int(input())
        
        # Subtract time from current player
        if white_turn:
            white_time -= move_time
        else:
            black_time -= move_time
        
        # Output current state
        output = f"White: {white_time}s Black: {black_time}s"
        
        # Check for flags
        if white_time < 0:
            output += " - White flags!"
        elif black_time < 0:
            output += " - Black flags!"
        
        print(output)
        
        # Switch turns
        white_turn = not white_turn
        
except EOFError:
    pass