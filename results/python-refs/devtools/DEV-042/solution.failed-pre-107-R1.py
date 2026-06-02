import sys
import hashlib
from collections import defaultdict

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    min_lines = int(lines[0])
    file_paths = lines[1:]
    return min_lines, file_paths

def read_file_lines(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.readlines()
    except:
        return []

def normalize_line(line):
    # Remove leading/trailing whitespace and convert to lowercase for comparison
    return line.strip().lower()

def get_code_blocks(file_path, min_lines):
    lines = read_file_lines(file_path)
    blocks = []
    
    for start_idx in range(len(lines)):
        for end_idx in range(start_idx + min_lines, len(lines) + 1):
            block_lines = []
            for i in range(start_idx, end_idx):
                normalized = normalize_line(lines[i])
                if normalized:  # Skip empty lines
                    block_lines.append(normalized)
            
            if len(block_lines) >= min_lines:
                # Create a hash of the block for comparison
                block_content = '\n'.join(block_lines)
                block_hash = hashlib.md5(block_content.encode()).hexdigest()
                blocks.append((block_hash, start_idx + 1, end_idx - start_idx, block_lines))
    
    return blocks

def find_duplicates(min_lines, file_paths):
    # Dictionary to store hash -> list of (file_path, start_line, num_lines)
    hash_to_locations = defaultdict(list)
    
    for file_path in file_paths:
        blocks = get_code_blocks(file_path, min_lines)
        for block_hash, start_line, num_lines, block_lines in blocks:
            hash_to_locations[block_hash].append((file_path, start_line, num_lines))
    
    # Find duplicates
    duplicates = []
    for block_hash, locations in hash_to_locations.items():
        if len(locations) > 1:
            # Sort by file path and line number
            locations.sort(key=lambda x: (x[0], x[1]))
            duplicates.append((locations[0][2], locations))
    
    return duplicates

def main():
    min_lines, file_paths = read_input()
    duplicates = find_duplicates(min_lines, file_paths)
    
    for num_lines, locations in duplicates:
        print(f"Duplicate block ({num_lines} lines):")
        for file_path, start_line, _ in locations:
            print(f"  {file_path}:{start_line}")

if __name__ == "__main__":
    main()