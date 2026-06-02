import sys

def main():
    data = sys.stdin.read().split('\n')
    if not data:
        return
    digits = data[0].strip()
    words = [w.strip() for w in data[1:] if w.strip()]
    mapping = {
        'A':'2','B':'2','C':'2',
        'D':'3','E':'3','F':'3',
        'G':'4','H':'4','I':'4',
        'J':'5','K':'5','L':'5',
        'M':'6','N':'6','O':'6',
        'P':'7','Q':'7','R':'7','S':'7',
        'T':'8','U':'8','V':'8',
        'W':'9','X':'9','Y':'9','Z':'9'
    }
    matches = []
    for w in words:
        wu = w.upper()
        if len(wu) != len(digits):
            continue
        if all(c in mapping for c in wu) and ''.join(mapping[c] for c in wu) == digits:
            matches.append(wu)
    matches = sorted(set(matches))
    print('\n'.join(matches))

main()
