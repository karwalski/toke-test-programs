import sys
import random

data = sys.stdin.read().split('\n')
sample_rate = float(data[0].strip())
seed = int(data[1].strip())
log_lines = data[2:]
if log_lines and log_lines[-1] == '':
    log_lines.pop()

if sample_rate >= 1.0:
    print('\n'.join(log_lines))
    sys.exit(0)

if sample_rate <= 0.0:
    sys.exit(0)

# Deterministic: pick every Nth line where N = round(1/rate), starting from 0
step = max(1, int(round(1.0 / sample_rate)))
out = [log_lines[i] for i in range(0, len(log_lines), step)]
print('\n'.join(out))