import sys, os

def setup():
    files = {
        '/tmp/sys053_a.txt': b'Hello, ',
        '/tmp/sys053_b.txt': b'World!\n',
        '/tmp/sys053_c.txt': b'Third file contents.',
    }
    for p, data in files.items():
        try:
            with open(p, 'wb') as f:
                f.write(data)
        except Exception:
            pass

def main():
    setup()
    data = sys.stdin.read().splitlines()
    lines = [l for l in data if l.strip() != '']
    if not lines:
        return
    out_path = lines[0]
    inputs = lines[1:]
    for p in inputs:
        if not os.path.isfile(p):
            print('ERROR: not found: ' + p)
            return
    total = 0
    with open(out_path, 'wb') as out:
        for p in inputs:
            with open(p, 'rb') as f:
                chunk = f.read()
                out.write(chunk)
                total += len(chunk)
    print('Merged: {} files into {}. Total: {} bytes.'.format(len(inputs), out_path, total))

main()
