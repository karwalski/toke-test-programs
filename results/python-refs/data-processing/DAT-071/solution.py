import sys

data = sys.stdin.read().strip('\n')
lines = data.split('\n')
out = []
for line in lines:
    fields = line.split('\t')
    new_fields = []
    for f in fields:
        if ',' in f or '"' in f or ' ' in f:
            f = '"' + f.replace('"', '""') + '"'
        new_fields.append(f)
    out.append(','.join(new_fields))
sys.stdout.write('\n'.join(out))