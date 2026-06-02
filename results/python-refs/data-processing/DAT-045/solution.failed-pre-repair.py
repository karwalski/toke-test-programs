import sys
import zlib

for line in sys.stdin:
    line = line.rstrip('\n')
    crc = zlib.crc32(line.encode('utf-8')) & 0xffffffff
    print(f"{crc:08x}\t{line}")