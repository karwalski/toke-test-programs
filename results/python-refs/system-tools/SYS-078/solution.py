import sys
import shutil
import os

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split(' ', 1)
    if len(parts) != 2:
        continue
    
    check_type, name = parts
    
    if check_type == 'cmd':
        if shutil.which(name) is not None:
            print(f"OK cmd {name}")
        else:
            print(f"MISSING cmd {name}")
    elif check_type == 'env':
        if name in os.environ:
            print(f"OK env {name}")
        else:
            print(f"MISSING env {name}")
    elif check_type == 'file':
        if os.path.isfile(name):
            print(f"OK file {name}")
        else:
            print(f"MISSING file {name}")