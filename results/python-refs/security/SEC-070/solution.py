import sys, json

def main():
    data = sys.stdin.read()
    zw = {'\u200b': 'ZWSP', '\u200c': 'ZWNJ', '\u200d': 'ZWJ', '\ufeff': 'BOM', '\u2060': 'WJ'}
    total = len(data)
    hidden_chars = [c for c in data if c in zw]
    visible = total - len(hidden_chars)
    counts = {}
    for c in hidden_chars:
        counts[zw[c]] = counts.get(zw[c], 0) + 1
    possible_encoding = None
    decoded = None
    # Try binary decode using ZWSP=0, ZWJ=1
    bits = []
    for c in hidden_chars:
        if c == '\u200b':
            bits.append('0')
        elif c == '\u200d':
            bits.append('1')
    hidden_bits = len(bits)
    if hidden_bits > 0 and hidden_bits % 8 == 0:
        possible_encoding = 'binary(ZWSP=0,ZWJ=1)'
        try:
            bs = ''.join(bits)
            byts = bytes(int(bs[i:i+8], 2) for i in range(0, len(bs), 8))
            s = byts.decode('utf-8')
            if all(32 <= ord(ch) < 127 or ch in '\n\r\t' for ch in s):
                decoded = s
        except Exception:
            decoded = None
    out = {
        'totalChars': total,
        'visibleChars': visible,
        'hiddenChars': len(hidden_chars),
        'hiddenBits': hidden_bits,
        'counts': counts,
        'possibleEncoding': possible_encoding,
        'decodedData': decoded,
    }
    print(json.dumps(out, sort_keys=True))

main()
