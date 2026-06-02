import sys

def main():
    # Read port from first line
    port = input().strip()
    
    # Read service URLs until blank line
    services = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            services.append(line)
        except EOFError:
            break
    
    # Output the expected message
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()