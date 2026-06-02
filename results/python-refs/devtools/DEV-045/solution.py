import sys
import re

def lint_dockerfile(content):
    lines = content.strip().split('\n')
    issues = []
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Check for latest tag
        if line.startswith('FROM') and ':latest' in line:
            issues.append(f"line {i}: [WARN] DL3007 - Using latest tag")
        
        # Check for apt-get update without cleanup
        if line.startswith('RUN') and 'apt-get update' in line:
            issues.append(f"line {i}: [WARN] DL3009 - Delete apt-get lists after install")
        
        # Check for separate RUN commands that could be combined
        if line.startswith('RUN') and i < len(lines):
            # Look for next RUN command
            for j in range(i, len(lines)):
                next_line = lines[j].strip()
                if next_line.startswith('RUN'):
                    issues.append(f"line {i}: [INFO] DL3015 - Combine RUN commands")
                    break
                elif next_line and not next_line.startswith('#'):
                    break
    
    return issues

def main():
    content = sys.stdin.read()
    issues = lint_dockerfile(content)
    
    for issue in issues:
        print(issue)
    
    print(f"{len(issues)} issues found")

if __name__ == "__main__":
    main()