import sys, subprocess, shutil

def get_status(unit):
    if not shutil.which('systemctl'):
        return ('N/A', 'N/A', '-')
    try:
        r = subprocess.run(['systemctl', 'show', unit, '--property=ActiveState,SubState,MainPID,LoadState'], capture_output=True, text=True, timeout=5)
    except Exception:
        return ('N/A', 'N/A', '-')
    if r.returncode != 0 and not r.stdout:
        return ('N/A', 'N/A', '-')
    props = {}
    for line in r.stdout.splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            props[k] = v
    load = props.get('LoadState', '')
    active = props.get('ActiveState', 'N/A')
    sub = props.get('SubState', 'N/A')
    pid = props.get('MainPID', '0')
    if load == 'not-found':
        return ('not-found', 'dead', '-')
    if pid == '0' or pid == '':
        pid = '-'
    if not active:
        active = 'N/A'
    if not sub:
        sub = 'N/A'
    return (active, sub, pid)

def main():
    data = sys.stdin.read().splitlines()
    out = []
    for line in data:
        unit = line.strip()
        if not unit:
            continue
        a, s, p = get_status(unit)
        out.append(f'{unit}: {a} sub={s} pid={p}')
    print('\n'.join(out))

main()
