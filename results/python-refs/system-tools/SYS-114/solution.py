import sys, re
from datetime import datetime, timedelta

data = sys.stdin.read()
if '---\n' in data:
    log_part, cfg_part = data.split('---\n', 1)
else:
    parts = data.rsplit('\n', 3)
    log_part = ''
    cfg_part = data
cfg_lines = cfg_part.strip().split('\n')
regex = cfg_lines[0]
bucket = cfg_lines[1].strip()

pat = re.compile(regex)

formats = [
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d',
]

def parse_ts(s):
    for f in formats:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return None

times = []
for line in log_part.splitlines():
    m = pat.search(line)
    if not m:
        continue
    dt = parse_ts(m.group(0))
    if dt is None:
        continue
    times.append(dt)

if not times:
    sys.exit(0)

def truncate(dt, b):
    if b == 'second':
        return dt.replace(microsecond=0)
    if b == 'minute':
        return dt.replace(second=0, microsecond=0)
    if b == 'hour':
        return dt.replace(minute=0, second=0, microsecond=0)
    raise ValueError

def step(b):
    if b == 'second': return timedelta(seconds=1)
    if b == 'minute': return timedelta(minutes=1)
    if b == 'hour': return timedelta(hours=1)

trunc = [truncate(t, bucket) for t in times]
counts = {}
for t in trunc:
    counts[t] = counts.get(t, 0) + 1

start = min(trunc)
end = max(trunc)
delta = step(bucket)

fmt = {'second': '%Y-%m-%dT%H:%M:%S', 'minute': '%Y-%m-%dT%H:%M', 'hour': '%Y-%m-%dT%H'}[bucket]

cur = start
out = []
while cur <= end:
    out.append(f"{cur.strftime(fmt)} {counts.get(cur, 0)}")
    cur += delta

print('\n'.join(out))
