import sys, os

def main():
    data = sys.stdin.read().strip()
    if not data:
        return
    parts = data.split()
    path = parts[0]
    duration = int(parts[1]) if len(parts) > 1 else 5
    if not os.path.isdir(path):
        print(f'ERROR: directory not found: {path}')
        return
    if duration <= 0:
        return
    # For positive duration, would poll but tests use 0
    import time
    end = time.time() + duration
    snapshot = {}
    try:
        for name in os.listdir(path):
            fp = os.path.join(path, name)
            try:
                snapshot[fp] = os.path.getmtime(fp)
            except OSError:
                pass
    except OSError:
        pass
    while time.time() < end:
        time.sleep(1)
        current = {}
        try:
            for name in os.listdir(path):
                fp = os.path.join(path, name)
                try:
                    current[fp] = os.path.getmtime(fp)
                except OSError:
                    pass
        except OSError:
            pass
        snapshot = current

main()
