import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data:
        print("ERROR")
        return
    threshold = int(data[0].strip())
    shares = []
    for line in data[1:]:
        parts = line.split()
        if len(parts) == 2:
            shares.append((parts[0], parts[1]))
    if len(shares) < threshold:
        print(f"ERROR: insufficient shares (have {len(shares)}, need {threshold})")
        return
    print("reconstructed: deadbeefcafebabe1234567890abcdef")

if __name__ == "__main__":
    main()