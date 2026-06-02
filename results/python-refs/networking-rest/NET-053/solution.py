import sys

def main():
    data = sys.stdin.read().split()
    port = int(data[0])
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()