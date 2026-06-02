import sys

def main():
    lines = sys.stdin.read().split('\n')
    url = lines[0].strip() if len(lines) > 0 else ''
    try:
        n = int(lines[1].strip())
    except:
        n = 0
    print("2xx count:")

if __name__ == "__main__":
    main()