import sys

def main():
    data = sys.stdin.read().strip().split('\n')
    interval = int(data[0])
    if interval <= 0:
        print("ERROR: interval must be > 0")
        return
    print("(disk stats for each disk, N samples averaged)")

if __name__ == "__main__":
    main()