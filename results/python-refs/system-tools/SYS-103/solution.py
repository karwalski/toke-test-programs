import sys, random, string

def main():
    data = sys.stdin.read().split('\n')
    length = int(data[0].strip())
    charset = data[1].strip()
    count = int(data[2].strip())
    seed = int(data[3].strip()) if len(data) > 3 and data[3].strip() else 0
    if charset == 'all':
        chars = string.ascii_letters + string.digits + '!@#$%^&*()-_=+[]{}'
    elif charset == 'alpha':
        chars = string.ascii_letters
    elif charset == 'numeric':
        chars = string.digits
    elif charset == 'alnum':
        chars = string.ascii_letters + string.digits
    elif charset == 'symbols':
        chars = '!@#$%^&*()-_=+[]{}'
    else:
        chars = string.ascii_letters + string.digits
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        out.append(''.join(rng.choice(chars) for _ in range(length)))
    print('\n'.join(out))

main()
