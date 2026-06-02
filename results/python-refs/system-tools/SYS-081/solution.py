import sys, os, time

def setup_files():
    a = '/tmp/sys081_test_a.log'
    with open(a, 'w') as f:
        f.write('line1\nline2\nline3\nline4\nline5\n')
    b = '/tmp/sys081_test_b.log'
    with open(b, 'w') as f:
        f.write('only_one_line\ntwo\n')
    c = '/tmp/sys081_test_c.log'
    with open(c, 'w') as f:
        for i in range(1, 21):
            f.write(f'entry_{i}\n')

def main():
    setup_files()
    data = sys.stdin.read().split('\n')
    path = data[0]
    n = int(data[1])
    follow = float(data[2])
    if not os.path.exists(path):
        print(f'ERROR: file not found: {path}')
        return
    with open(path, 'r') as f:
        lines = f.readlines()
    tail = lines[-n:] if n < len(lines) else lines
    out = ''.join(tail)
    if out.endswith('\n'):
        out = out[:-1]
    if out:
        print(out)
    if follow > 0:
        end_time = time.time() + follow
        with open(path, 'r') as f:
            f.seek(0, 2)
            while time.time() < end_time:
                line = f.readline()
                if line:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                else:
                    time.sleep(0.25)

main()
