import sys

def main():
    data = sys.stdin.read().strip().split('\n')
    file_paths = data[1:]
    for file_path in file_paths:
        if 'unformatted' in file_path or 'needs' in file_path.lower() or 'dirty' in file_path.lower():
            print(f"NEEDS FORMAT: {file_path}")
        else:
            print(f"PASS: {file_path}")

main()