import sys

def main():
    # Read all input
    input_lines = []
    for line in sys.stdin:
        input_lines.append(line.rstrip('\n'))
    
    # Find the separator
    separator_idx = -1
    for i, line in enumerate(input_lines):
        if line == '---':
            separator_idx = i
            break
    
    if separator_idx == -1:
        return
    
    # Extract license header template and file paths
    license_header = '\n'.join(input_lines[:separator_idx])
    file_paths = input_lines[separator_idx + 1:]
    
    # Check each file
    for file_path in file_paths:
        if not file_path.strip():
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Check if file starts with the license header
            if file_content.startswith(license_header):
                print(f"PASS: {file_path}")
            else:
                print(f"FAIL: {file_path} - missing license header")
                
        except (FileNotFoundError, IOError, PermissionError):
            print(f"FAIL: {file_path} - missing license header")

if __name__ == "__main__":
    main()