import sys, time

def main():
    data = sys.stdin.read()
    if '\n' in data:
        first, rest = data.split('\n', 1)
    else:
        first, rest = data, ''
    try:
        rate = int(first.strip())
    except ValueError:
        sys.stdout.write('ERROR: rate must be > 0')
        return
    if rate <= 0:
        sys.stdout.write('ERROR: rate must be > 0')
        return
    payload = rest.encode('utf-8')
    chunk = max(1, rate // 10) if rate >= 10 else 1
    delay = chunk / rate
    i = 0
    out = sys.stdout.buffer
    while i < len(payload):
        piece = payload[i:i+chunk]
        out.write(piece)
        out.flush()
        i += chunk
        if i < len(payload):
            time.sleep(delay)

main()
