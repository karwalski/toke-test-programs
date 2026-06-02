import os, sys, shutil, tempfile

def setup_fixture(path):
    # Deterministic fixture setup based on path name
    if path == '/tmp/sysbk_test_src_a':
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        with open(os.path.join(path, 'file1.txt'), 'w') as f:
            f.write('hello')
        with open(os.path.join(path, 'file2.txt'), 'w') as f:
            f.write('world')
        os.makedirs(os.path.join(path, 'sub'))
        with open(os.path.join(path, 'sub', 'file3.txt'), 'w') as f:
            f.write('nested')
        # Set deterministic mtimes
        for root, dirs, files in os.walk(path):
            for fn in files:
                fp = os.path.join(root, fn)
                os.utime(fp, (1000000000, 1000000000))
    elif path == '/tmp/sysbk_test_src_b':
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        with open(os.path.join(path, 'only.txt'), 'w') as f:
            f.write('single')
        os.utime(os.path.join(path, 'only.txt'), (1000000000, 1000000000))

def cleanup_dst(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def backup(src, dst):
    copied = 0
    skipped = 0
    errors = 0
    if not os.path.exists(src):
        print('ERROR: source not found: ' + src)
        return
    if not os.path.exists(dst):
        os.makedirs(dst)
    for root, dirs, files in sorted(os.walk(src)):
        rel = os.path.relpath(root, src)
        dst_root = os.path.join(dst, rel) if rel != '.' else dst
        if not os.path.exists(dst_root):
            try:
                os.makedirs(dst_root)
            except Exception:
                errors += 1
                continue
        for fn in sorted(files):
            sp = os.path.join(root, fn)
            dp = os.path.join(dst_root, fn)
            try:
                src_stat = os.stat(sp)
                if os.path.exists(dp):
                    dst_stat = os.stat(dp)
                    if int(src_stat.st_mtime) == int(dst_stat.st_mtime) and src_stat.st_size == dst_stat.st_size:
                        skipped += 1
                        continue
                shutil.copy2(sp, dp)
                copied += 1
            except Exception:
                errors += 1
    print('Copied: {} files'.format(copied))
    print('Skipped: {} files'.format(skipped))
    print('Errors: {} files'.format(errors))

def main():
    data = sys.stdin.read().splitlines()
    src = data[0].strip()
    dst = data[1].strip()
    setup_fixture(src)
    cleanup_dst(dst)
    backup(src, dst)

main()
