import sys

for line in sys.stdin:
    line = line.rstrip('\n')
    print(f'<p>{line}</p>')