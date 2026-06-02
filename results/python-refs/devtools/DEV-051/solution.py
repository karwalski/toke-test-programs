import sys
from collections import defaultdict

def main():
    file_paths = []
    for line in sys.stdin:
        file_paths.append(line.strip())
    
    # Dictionary to count occurrences of each line across all files
    line_counts = defaultdict(int)
    # Dictionary to store lines per file
    file_lines = {}
    
    # Read all files and count line occurrences
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                # Strip whitespace and filter out empty lines
                lines = [line.strip() for line in lines if line.strip()]
                file_lines[file_path] = lines
                
                for line in lines:
                    line_counts[line] += 1
        except:
            file_lines[file_path] = []
    
    # Calculate duplicated lines per file
    total_lines = 0
    total_duplicated = 0
    
    for file_path in file_paths:
        lines = file_lines.get(file_path, [])
        duplicated_count = 0
        
        for line in lines:
            if line_counts[line] > 1:
                duplicated_count += 1
        
        total_lines += len(lines)
        total_duplicated += duplicated_count
        
        if len(lines) > 0:
            percentage = round(duplicated_count * 100 / len(lines))
        else:
            percentage = 0
            
        print(f"{file_path}: {len(lines)} lines ({percentage}% duplicated)")
    
    # Calculate overall duplication rate
    if total_lines > 0:
        overall_percentage = round(total_duplicated * 100 / total_lines)
    else:
        overall_percentage = 0
    
    print(f"Overall: {overall_percentage}% duplication")

if __name__ == "__main__":
    main()