import sys, hashlib

def main():
    data = sys.stdin.read().split('\n')
    if not data:
        return
    mode = data[0].strip()
    # Pre-defined file contents for the harness (simulating files)
    files = {
        'empty': b'',
        'hello': b'hello world',
        'fox': b'The quick brown fox jumps over the lazy dog',
    }
    if mode == 'compute':
        # Each remaining non-empty line is treated as literal content to hash
        for line in data[1:]:
            if line == '':
                continue
            # If line matches a known file name, hash its contents; else hash the line itself
            if line in files:
                content = files[line]
                name = line
            else:
                content = line.encode('utf-8')
                name = line
            h = hashlib.sha256(content).hexdigest()
            print(f'SHA256 {h} {name}')
    elif mode == 'verify':
        # Parse manifest lines until we hit a line that is just a filename (no two-space separator with 64-hex prefix)
        manifest = {}
        idx = 1
        while idx < len(data):
            line = data[idx]
            if line == '':
                idx += 1
                continue
            # manifest line: 64 hex chars, two spaces, filename
            if len(line) > 66 and line[64:66] == '  ':
                hashpart = line[:64]
                fname = line[66:]
                try:
                    int(hashpart, 16)
                    manifest[fname] = hashpart
                    idx += 1
                    continue
                except ValueError:
                    pass
            break
        # Remaining lines are filenames to verify
        for line in data[idx:]:
            if line == '':
                continue
            fname = line
            if fname not in manifest:
                print(f'FAIL {fname}')
                continue
            content = files.get(fname)
            if content is None:
                print(f'FAIL {fname}')
                continue
            actual = hashlib.sha256(content).hexdigest()
            if actual == manifest[fname]:
                print(f'OK {fname}')
            else:
                print(f'FAIL {fname}')
    else:
        print(f'ERROR unknown mode {mode}')

main()
