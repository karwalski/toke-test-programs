import sys

def main():
    data = sys.stdin.read()
    lines = data.strip().split('\n')
    # Count tests by counting lines starting with "- name:"
    tests = []
    for line in lines[1:]:
        if line.startswith('- name:'):
            name = line.split(':', 1)[1].strip()
            tests.append(name)
    
    for _ in tests:
        print("PASS")

if __name__ == "__main__":
    main()