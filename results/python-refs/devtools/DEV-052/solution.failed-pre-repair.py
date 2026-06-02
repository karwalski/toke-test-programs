import sys
import os

for line in sys.stdin:
    source_file = line.strip()
    if not source_file:
        continue
    
    # Get the directory and filename
    dir_path = os.path.dirname(source_file)
    filename = os.path.basename(source_file)
    
    # Split filename and extension
    name, ext = os.path.splitext(filename)
    
    # Create test filename
    test_filename = f"{name}_test{ext}"
    
    # Create full test file path
    if dir_path:
        test_file_path = os.path.join(dir_path, test_filename)
    else:
        test_file_path = test_filename
    
    # Check if test file exists
    if os.path.exists(test_file_path):
        print(f"{source_file} -> {test_file_path}")
    else:
        print(f"{source_file} -> MISSING")