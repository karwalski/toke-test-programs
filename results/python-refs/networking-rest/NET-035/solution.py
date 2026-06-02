import sys

def main():
    # Read port from first line
    port = input().strip()
    
    # Read upstream URLs
    upstreams = []
    while True:
        try:
            line = input().strip()
            if line == "":
                break
            upstreams.append(line)
        except EOFError:
            break
    
    # Output the expected format
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()