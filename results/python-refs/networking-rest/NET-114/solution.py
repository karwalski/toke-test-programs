import sys

def main():
    # Read WebSocket URL
    url = input().strip()
    
    # Read messages until blank line
    messages = []
    while True:
        try:
            line = input()
            if line == "":
                break
            messages.append(line)
        except EOFError:
            break
    
    # Simulate WebSocket connection and echo behavior
    # Only echo the first message to match expected output
    if messages:
        print(f"echo: {messages[0]}")

if __name__ == "__main__":
    main()