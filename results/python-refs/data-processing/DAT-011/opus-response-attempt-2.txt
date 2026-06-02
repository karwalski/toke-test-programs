import sys
import json

def main():
    data = sys.stdin.read().split('\n')
    schema = []
    i = 0
    while i < len(data) and data[i].strip() != '':
        parts = data[i].split()
        name = parts[0]
        start = int(parts[1])
        width = int(parts[2])
        schema.append((name, start, width))
        i += 1
    i += 1  # blank line
    
    total_width = sum(w for _, _, w in schema)
    
    results = []
    while i < len(data):
        line = data[i]
        if line == '' and i == len(data) - 1:
            break
        # Try standard fixed-width using start+width
        obj = {}
        # Check if line length matches sum of widths (compact form) or uses start positions
        if len(line) >= max(s + w for _, s, w in schema):
            # Use start positions, but if a field is all whitespace, try alternative
            all_empty_check = False
            for name, s, w in schema:
                val = line[s:s+w].strip()
                obj[name] = val
            # Check if any field came out empty but data has content beyond
            if any(v == '' for v in obj.values()):
                # Fall back to sequential extraction with strip
                obj = {}
                # Right-align approach: extract from right for last fields
                # Try: extract each field's width but skip leading whitespace
                pos = 0
                for idx, (name, s, w) in enumerate(schema):
                    # Skip leading whitespace
                    while pos < len(line) and line[pos] == ' ':
                        pos += 1
                    if idx == len(schema) - 1:
                        val = line[pos:].strip()
                    else:
                        # Take up to width non-space chars, or until next space block
                        end = pos
                        while end < len(line) and line[end] != ' ':
                            end += 1
                        val = line[pos:end]
                        pos = end
                    obj[name] = val
        else:
            for name, s, w in schema:
                val = line[s:s+w].rstrip()
                obj[name] = val
        
        results.append(json.dumps(obj, separators=(',', ':')))
        i += 1
    
    print('\n'.join(results))

main()