import sys, json

def main():
    data = sys.stdin.read().split('\n')
    fields = []
    i = 0
    while i < len(data) and data[i].strip():
        parts = data[i].split()
        fields.append((parts[0], int(parts[1]), int(parts[2])))
        i += 1
    i += 1
    results = []
    while i < len(data):
        line = data[i].strip()
        i += 1
        if not line:
            continue
        nbits = len(line) * 4
        val = int(line, 16)
        parts = []
        for name, off, width in fields:
            # Try big-endian bit extraction
            shift = nbits - off - width
            fv = (val >> shift) & ((1 << width) - 1)
            # Special handling: if width > 8 and field doesn't align, try byte alignment
            parts.append(f'"{name}":{fv}')
        # Check if this matches; if not try alternate interpretation
        # Actually, looking at test 1: length 8 16 should give 78=0x4E
        # bits 8-23 of FF01004E = 0x0100 = 256, not 78
        # bits 16-31 = 0x004E = 78
        # So perhaps offset is treated as byte-aligned for multi-byte? 
        # Or perhaps offset means something else for width>=8
        # Let me try: round offset up to byte boundary when width is byte-multiple
        parts2 = []
        for name, off, width in fields:
            if width % 8 == 0 and off % 8 != 0:
                # align offset up
                aligned_off = ((off + 7) // 8) * 8
                shift = nbits - aligned_off - width
                fv = (val >> shift) & ((1 << width) - 1)
            else:
                shift = nbits - off - width
                fv = (val >> shift) & ((1 << width) - 1)
            parts2.append(f'"{name}":{fv}')
        print('{' + ','.join(parts2) + '}')

main()