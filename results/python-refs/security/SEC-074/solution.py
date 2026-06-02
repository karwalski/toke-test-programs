import sys, json

COMMON = {'password','123456','12345678','qwerty','abc123','letmein','admin','welcome','monkey','iloveyou'}
SPECIALS = set('!@#$%^&*()-_=+[]{};:,.<>/?\\|`~\'"')

def validate(pw, pol):
    v = []
    if 'minLength' in pol and len(pw) < pol['minLength']:
        v.append('minLength')
    if 'maxLength' in pol and len(pw) > pol['maxLength']:
        v.append('maxLength')
    if pol.get('requireUpper') and not any(c.isupper() for c in pw):
        v.append('requireUpper')
    if pol.get('requireLower') and not any(c.islower() for c in pw):
        v.append('requireLower')
    if pol.get('requireDigit') and not any(c.isdigit() for c in pw):
        v.append('requireDigit')
    if pol.get('requireSpecial') and not any(c in SPECIALS for c in pw):
        v.append('requireSpecial')
    if 'maxRepeating' in pol:
        m = pol['maxRepeating']
        run = 1
        bad = False
        for i in range(1, len(pw)):
            if pw[i] == pw[i-1]:
                run += 1
                if run > m:
                    bad = True
                    break
            else:
                run = 1
        if bad:
            v.append('maxRepeating')
    if pol.get('disallowCommon') and pw.lower() in COMMON:
        v.append('disallowCommon')
    return v

def main():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    pol = json.loads(data[0])
    for line in data[1:]:
        if line == '':
            break
        v = validate(line, pol)
        if not v:
            print('PASS')
        else:
            print('FAIL ' + ','.join(v))

main()
