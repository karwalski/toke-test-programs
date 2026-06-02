import sys
import zlib

data = sys.stdin.read()
if data == '':
    print('00000000\t')
    sys.exit(0)

lines = data.split('\n')

out = []
for line in lines:
    crc = zlib.crc32(line.encode('utf-8')) & 0xffffffff
    out.append(f"{crc:08x}\t{line}")
sys.stdout.write('\n'.join(out))