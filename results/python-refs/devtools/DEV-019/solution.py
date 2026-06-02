import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    files = [f.strip() for f in data[1:] if f.strip()]
    if len(files) >= 2:
        print(f"{files[0]} -> {files[1]}")

if __name__ == "__main__":
    main()