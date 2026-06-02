import sys

def parse_meminfo(text):
    info = {}
    for line in text.splitlines():
        parts = line.split(':')
        if len(parts) < 2:
            continue
        key = parts[0].strip()
        val = parts[1].strip().split()
        if val:
            try:
                info[key] = int(val[0])
            except ValueError:
                pass
    return info

def parse_status(text):
    info = {}
    for line in text.splitlines():
        parts = line.split(':')
        if len(parts) < 2:
            continue
        key = parts[0].strip()
        val = parts[1].strip().split()
        if val:
            try:
                info[key] = int(val[0])
            except ValueError:
                pass
    return info

def kb_to_mb(kb):
    return round(kb / 1024.0, 2)

MOCK_MEMINFO = '''MemTotal:        8192000 kB
MemFree:         2048000 kB
MemAvailable:    4096000 kB
Buffers:          102400 kB
Cached:          1024000 kB
'''

MOCK_PROCS = {
    1: {
        'status': 'Name:\tinit\nVmRSS:\t   12345 kB\nVmSize:\t  234567 kB\nRssShmem:\t    2048 kB\nRssFile:\t    4096 kB\nRssAnon:\t    6201 kB\n',
    },
    2: {
        'status': 'Name:\tkthreadd\nVmRSS:\t     512 kB\nVmSize:\t   10240 kB\nRssShmem:\t     128 kB\nRssFile:\t     256 kB\nRssAnon:\t     128 kB\n',
    },
}

def main():
    data = sys.stdin.read()
    line = data.strip()
    mi = parse_meminfo(MOCK_MEMINFO)
    total = mi.get('MemTotal', 0)
    free = mi.get('MemFree', 0)
    used = total - free
    print('System: total={} free={} used={}'.format(kb_to_mb(total), kb_to_mb(free), kb_to_mb(used)))
    if line == '':
        return
    try:
        pid = int(line)
    except ValueError:
        print('NOT FOUND')
        return
    if pid not in MOCK_PROCS:
        print('NOT FOUND')
        return
    st = parse_status(MOCK_PROCS[pid]['status'])
    rss = st.get('VmRSS', 0)
    vsz = st.get('VmSize', 0)
    shared = st.get('RssShmem', 0) + st.get('RssFile', 0)
    private = st.get('RssAnon', 0)
    print('PID {}: rss={} vsz={} shared={} private={}'.format(pid, kb_to_mb(rss), kb_to_mb(vsz), kb_to_mb(shared), kb_to_mb(private)))

main()
