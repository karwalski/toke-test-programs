import sys, re

def main():
    data = sys.stdin.read().split('\n')
    if not data:
        return
    pattern = data[0]
    rx = re.compile(pattern)
    # Remaining lines: split by '---' separators into file groups
    files = []
    current = []
    for line in data[1:]:
        if line == '---':
            if current:
                files.append(current)
                current = []
        else:
            current.append(line)
    if current:
        # strip trailing empty line from final split
        while current and current[-1] == '':
            current.pop()
        if current:
            files.append(current)
    if not files and current == []:
        pass

    # Build entries: each entry is (timestamp_str, file_index, order_in_file, [lines])
    # Lines without timestamp attach to previous entry in same file.
    entries = []
    for fi, lines in enumerate(files):
        order = 0
        cur_entry = None
        for ln in lines:
            m = rx.match(ln)
            if m:
                cur_entry = [m.group(0), fi, order, [ln]]
                entries.append(cur_entry)
                order += 1
            else:
                if cur_entry is not None:
                    cur_entry[3].append(ln)
                # else: orphan continuation before any timestamp - skip

    # Dedupe: same timestamp + same block content
    seen = set()
    unique = []
    for e in entries:
        key = (e[0], tuple(e[3]))
        if key in seen:
            continue
        seen.add(key)
        unique.append(e)

    # Stable sort by timestamp (string sort works for ISO formats)
    unique.sort(key=lambda e: e[0])

    out = []
    for e in unique:
        out.extend(e[3])
    sys.stdout.write('\n'.join(out))
    if out:
        sys.stdout.write('\n')

main()
