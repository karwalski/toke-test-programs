import sys
import re

def main():
    lines = sys.stdin.read().strip().split('\n')
    
    total_tasks = 0
    completed_tasks = 0
    incomplete_titles = []
    
    for line in lines:
        # Match task list items: - [x] or - [ ]
        match = re.match(r'^- \[([ x])\] (.+)$', line)
        if match:
            total_tasks += 1
            checkbox = match.group(1)
            title = match.group(2)
            
            if checkbox == 'x':
                completed_tasks += 1
            else:
                incomplete_titles.append(title)
    
    # Output summary
    print(f"{completed_tasks}/{total_tasks} completed")
    
    # Output incomplete items
    for title in incomplete_titles:
        print(title)

if __name__ == "__main__":
    main()