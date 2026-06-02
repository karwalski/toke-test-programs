import os
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split(' ', 2)
    operation = parts[0]
    
    if operation == "normalize":
        path = parts[1]
        result = os.path.normpath(path)
        print(result)
    
    elif operation == "join":
        path1 = parts[1]
        path2 = parts[2]
        result = os.path.join(path1, path2)
        print(result)
    
    elif operation == "basename":
        path = parts[1]
        result = os.path.basename(path)
        print(result)
    
    elif operation == "dirname":
        path = parts[1]
        result = os.path.dirname(path)
        print(result)
    
    elif operation == "ext":
        path = parts[1]
        result = os.path.splitext(path)[1]
        print(result)
    
    elif operation == "exists":
        path = parts[1]
        result = os.path.exists(path)
        print(result)