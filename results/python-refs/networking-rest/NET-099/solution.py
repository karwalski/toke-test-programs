import sys

def main():
    lines = sys.stdin.read().strip().split('\n')
    port = int(lines[0])
    total_items = int(lines[1])
    
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()