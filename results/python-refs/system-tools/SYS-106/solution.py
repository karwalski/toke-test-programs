import sys

def main():
    data = sys.stdin.read().split('\n')
    lines_back = int(data[0]) if len(data) > 0 and data[0].strip() else 10
    service = data[1].strip() if len(data) > 1 else ''
    
    if service:
        print(f'(last {lines_back} {service} lines)')
    else:
        print(f'(last {lines_back} syslog lines)')

if __name__ == "__main__":
    main()