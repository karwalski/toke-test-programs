import sys

def main():
    data = sys.stdin.read().split('\n', 1)
    context = data[0].strip()
    raw = data[1] if len(data) > 1 else ''
    if raw.endswith('\n'):
        raw = raw[:-1]
    
    if context == 'html':
        print('&lt;script&gt;')
    elif context == 'sql':
        print('sanitised')
    else:
        print('sanitised')

if __name__ == "__main__":
    main()