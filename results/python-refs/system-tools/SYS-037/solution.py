import sys, re

def main():
    data = sys.stdin.read().split('\n')
    # Format: line 0 = pattern, then '---', then filenames (| separated), then '---', then content blocks split by --FILE--, then '---', then recursive flag
    pattern = data[0]
    # find separators
    idx = 1
    assert data[idx] == '---'
    idx += 1
    fnames = data[idx].split('|')
    idx += 1
    # collect content until next '---'
    content_lines = []
    while idx < len(data) and data[idx] != '---':
        content_lines.append(data[idx])
        idx += 1
    # idx is at '---'
    idx += 1
    recursive = data[idx] if idx < len(data) else 'no'
    # split content into files by --FILE-- separator
    files = []
    cur = []
    for ln in content_lines:
        if ln == '--FILE--':
            files.append(cur)
            cur = []
        else:
            cur.append(ln)
    files.append(cur)
    # pair filenames with files
    regex = re.compile(pattern)
    out = []
    for fname, flines in zip(fnames, files):
        for i, line in enumerate(flines, start=1):
            if regex.search(line):
                out.append(f'{fname}:{i}:{line}')
    sys.stdout.write('\n'.join(out))
    if out:
        sys.stdout.write('\n')

main()
