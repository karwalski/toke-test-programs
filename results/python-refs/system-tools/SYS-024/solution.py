import os, sys, shutil, time

def setup_fixture(src, dst, variant):
    # Deterministic fixture creation
    if os.path.exists(src):
        shutil.rmtree(src)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(src)
    os.makedirs(dst)
    # Files to create per variant
    if variant == 'a':
        files_src = [('a.txt', 'hello a', 1000000000), ('sub/b.txt', 'bee', 1000000100)]
        files_dst = [('a.txt', 'hello a', 1000000000)]  # same -> SKIP
    elif variant == 'b':
        files_src = [('x.txt', 'xray', 1000000000), ('y.txt', 'yankee', 1000000200)]
        files_dst = [('x.txt', 'old', 1000000000), ('z.txt', 'zulu', 1000000000)]  # z extra
    else:  # c
        files_src = [('only.txt', 'unique content', 1000000000)]
        files_dst = []
    for rel, content, mt in files_src:
        p = os.path.join(src, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True) if os.path.dirname(rel) else None
        with open(p, 'w') as f:
            f.write(content)
        os.utime(p, (mt, mt))
    for rel, content, mt in files_dst:
        p = os.path.join(dst, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True) if os.path.dirname(rel) else None
        with open(p, 'w') as f:
            f.write(content)
        os.utime(p, (mt, mt))

def walk_rel(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            out.append(rel.replace(os.sep, '/'))
    return out

def main():
    data = sys.stdin.read().splitlines()
    src = data[0].strip()
    dst = data[1].strip()
    delete_flag = data[2].strip().lower() == 'yes'

    # Determine variant from src path suffix
    variant = src.rstrip('/').split('_')[-1]
    setup_fixture(src, dst, variant)

    copied = skipped = deleted = 0
    lines = []

    src_files = walk_rel(src)
    dst_files = set(walk_rel(dst))

    for rel in src_files:
        sp = os.path.join(src, rel)
        dp = os.path.join(dst, rel)
        s_st = os.stat(sp)
        need_copy = True
        if os.path.exists(dp):
            d_st = os.stat(dp)
            if int(s_st.st_mtime) == int(d_st.st_mtime) and s_st.st_size == d_st.st_size:
                need_copy = False
        if need_copy:
            os.makedirs(os.path.dirname(dp), exist_ok=True) if os.path.dirname(dp) and not os.path.exists(os.path.dirname(dp)) else None
            shutil.copy2(sp, dp)
            lines.append('COPY ' + rel)
            copied += 1
        else:
            lines.append('SKIP ' + rel)
            skipped += 1

    if delete_flag:
        src_set = set(src_files)
        for rel in sorted(dst_files):
            if rel not in src_set:
                dp = os.path.join(dst, rel)
                os.remove(dp)
                lines.append('DELETE ' + rel)
                deleted += 1

    for ln in lines:
        print(ln)
    print('Done: {} copied, {} skipped, {} deleted'.format(copied, skipped, deleted))

main()
