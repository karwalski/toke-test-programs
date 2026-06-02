import os
import sys

def resolve_symlink_chain(path):
    """Resolve a symlink chain and return all steps."""
    steps = [path]
    current = path
    seen = set()
    
    while os.path.islink(current):
        if current in seen:
            # Circular symlink detected
            steps.append("NOTFOUND")
            return steps
        
        seen.add(current)
        try:
            target = os.readlink(current)
            # If target is relative, make it absolute relative to the directory of current
            if not os.path.isabs(target):
                target = os.path.join(os.path.dirname(current), target)
                target = os.path.normpath(target)
            
            steps.append(target)
            current = target
        except (OSError, FileNotFoundError):
            steps.append("NOTFOUND")
            return steps
    
    # Check if final target exists
    if not os.path.exists(current):
        if steps[-1] != "NOTFOUND":
            steps.append("NOTFOUND")
    
    return steps

def main():
    for line in sys.stdin:
        path = line.strip()
        if not path:
            continue
            
        steps = resolve_symlink_chain(path)
        output = " -> ".join(steps)
        print(output)

if __name__ == "__main__":
    main()