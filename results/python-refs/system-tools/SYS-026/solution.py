import sys, re

def main():
    data = sys.stdin.read().splitlines()
    # Split on a line that is exactly '---'
    try:
        sep = data.index('---')
    except ValueError:
        print('Summary: 0 files renamed.')
        return
    files = data[:sep]
    rest = data[sep+1:]
    if len(rest) < 3:
        print('Summary: 0 files renamed.')
        return
    pattern = rest[0]
    replacement = rest[1]
    dry_run = rest[2].strip().lower() == 'yes'
    try:
        rx = re.compile(pattern)
    except re.error:
        print('Summary: 0 files renamed.')
        return
    # Simulate filesystem state
    existing = list(files)
    existing_set = set(existing)
    count = 0
    out_lines = []
    for name in files:
        if not rx.search(name):
            continue
        new_name = rx.sub(replacement, name)
        if new_name == name:
            continue
        # Collision check against current state (excluding the file itself)
        others = set(existing_set)
        others.discard(name)
        if new_name in others:
            continue
        out_lines.append('RENAME {} -> {}'.format(name, new_name))
        count += 1
        if not dry_run:
            existing_set.discard(name)
            existing_set.add(new_name)
            for i, n in enumerate(existing):
                if n == name:
                    existing[i] = new_name
                    break
    for line in out_lines:
        print(line)
    print('Summary: {} files renamed.'.format(count))

main()
