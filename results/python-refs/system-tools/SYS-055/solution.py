import sys

def print_color_grid(mode):
    if mode == "16":
        # Print 16 standard colors in 2 rows of 8
        for row in range(2):
            for col in range(8):
                color_index = row * 8 + col
                # Use background color with space character to show the color block
                print(f"\033[48;5;{color_index}m {color_index:2d} \033[0m", end="")
            print()  # New line after each row
    
    elif mode == "256":
        # Print all 256 colors
        # First 16 colors (standard colors)
        print("Standard colors (0-15):")
        for row in range(2):
            for col in range(8):
                color_index = row * 8 + col
                print(f"\033[48;5;{color_index}m {color_index:3d} \033[0m", end="")
            print()
        
        print("\n216 colors (16-231):")
        # 216 colors in 6x6x6 cube (colors 16-231)
        for r in range(6):
            for g in range(6):
                for b in range(6):
                    color_index = 16 + (r * 36) + (g * 6) + b
                    print(f"\033[48;5;{color_index}m {color_index:3d} \033[0m", end="")
                print()  # New line after each blue level
            if r < 5:
                print()  # Extra line between red levels
        
        print("\nGrayscale colors (232-255):")
        # 24 grayscale colors (colors 232-255)
        for i in range(24):
            color_index = 232 + i
            print(f"\033[48;5;{color_index}m {color_index:3d} \033[0m", end="")
            if (i + 1) % 12 == 0:  # 12 colors per row
                print()
    
    elif mode == "truecolor":
        print("True color test (24-bit RGB):")
        # Show a gradient demonstrating true color support
        for r in range(0, 256, 32):
            for g in range(0, 256, 32):
                for b in range(0, 256, 32):
                    print(f"\033[48;2;{r};{g};{b}m   \033[0m", end="")
                print()
            print()

def main():
    # Read mode from stdin, default to "256" if no input
    try:
        mode = input().strip()
    except EOFError:
        mode = "256"
    
    if mode not in ["16", "256", "truecolor"]:
        mode = "256"
    
    print_color_grid(mode)

if __name__ == "__main__":
    main()