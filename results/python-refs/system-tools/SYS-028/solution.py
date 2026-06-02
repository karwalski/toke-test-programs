import sys, os, json

# Deterministic in-memory trash simulation.
# Files are virtual: TRASH records the filepath; deletion time is a monotonic counter.

def main():
    data = sys.stdin.read().splitlines()
    trash = {}  # name -> {'original_path':..., 'deleted_at':int}
    counter = 0
    out = []
    for line in data:
        line = line.rstrip('\n')
        if not line.strip():
            continue
        parts = line.split(' ', 1)
        cmd = parts[0]
        if cmd == 'TRASH':
            path = parts[1].strip()
            name = os.path.basename(path)
            # handle collision by suffixing
            final = name
            i = 1
            while final in trash:
                final = name + '.' + str(i)
                i += 1
            counter += 1
            trash[final] = {'original_path': path, 'deleted_at': counter}
            out.append('Moved to trash: ' + final)
        elif cmd == 'LIST':
            if not trash:
                out.append('(empty)')
            else:
                for n in sorted(trash.keys()):
                    e = trash[n]
                    out.append(n + ' ' + e['original_path'] + ' ' + str(e['deleted_at']))
        elif cmd == 'RESTORE':
            name = parts[1].strip()
            if name in trash:
                p = trash[name]['original_path']
                del trash[name]
                out.append('Restored to ' + p)
            else:
                out.append('Not found: ' + name)
        elif cmd == 'EMPTY':
            n = len(trash)
            trash.clear()
            out.append('Emptied ' + str(n) + ' items.')
        else:
            out.append('Unknown command')
    sys.stdout.write('\n'.join(out) + ('\n' if out else ''))

main()
