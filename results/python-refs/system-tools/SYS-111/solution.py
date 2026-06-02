import sys
import os

def main():
    lines = [line.strip() for line in sys.stdin.read().strip().split('\n')]
    
    owner_group = lines[0]
    recursive = lines[1].lower() == 'yes'
    dry_run = lines[2].lower() == 'yes'
    paths = lines[3:]
    
    items_changed = 0
    
    for path in paths:
        if recursive and os.path.isdir(path):
            # Process directory recursively
            for root, dirs, files in os.walk(path):
                # Process the directory itself
                print(f"chown {owner_group} {root}")
                items_changed += 1
                
                # Process all files in the directory
                for file in files:
                    file_path = os.path.join(root, file)
                    print(f"chown {owner_group} {file_path}")
                    items_changed += 1
        else:
            # Process single file/directory
            print(f"chown {owner_group} {path}")
            items_changed += 1
    
    print(f"Summary: {items_changed} items changed.")

if __name__ == "__main__":
    main()