import sys, hashlib

def main():
    data = sys.stdin.read().split('\n')
    idx = 0
    n = int(data[idx]); idx += 1
    files = {}
    for _ in range(n):
        line = data[idx]; idx += 1
        name, content = line.split('|', 1)
        files[name] = content
    action = data[idx].strip()

    hashes = {}
    for name in sorted(files.keys()):
        h = hashlib.sha256(files[name].encode()).hexdigest()
        hashes.setdefault(h, []).append(name)

    groups = [g for g in hashes.values() if len(g) > 1]
    groups.sort(key=lambda g: g[0])

    removed = 0
    if not groups:
        print('No duplicates found')
    else:
        for g in groups:
            keep = g[0]
            for dup in g[1:]:
                print(f'DUPLICATE {dup} (keeping {keep})')
                if action == 'delete':
                    removed += 1

    if action == 'delete':
        print(f'Summary: {len(groups)} duplicate groups, {removed} files removed')
    else:
        print(f'Summary: {len(groups)} duplicate groups, 0 files removed')

main()
