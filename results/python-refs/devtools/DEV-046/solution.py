import sys
from collections import defaultdict

def main():
    author_counts = defaultdict(int)
    total_lines = 0
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(' ', 3)
        if len(parts) >= 4:
            author = parts[1]
            author_counts[author] += 1
            total_lines += 1
    
    # Sort by line count descending, then by author name for consistent ordering
    sorted_authors = sorted(author_counts.items(), key=lambda x: (-x[1], x[0]))
    
    for author, count in sorted_authors:
        percentage = round(100 * count / total_lines)
        print(f"{author}: {count} lines ({percentage}%)")

if __name__ == "__main__":
    main()