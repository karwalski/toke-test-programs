import sys

def main():
    data = sys.stdin.read().split()
    interval = int(data[0])
    if interval <= 0:
        print("ERROR: interval must be > 0")
        return
    print("(per-interface bandwidth per sample)")

if __name__ == "__main__":
    main()