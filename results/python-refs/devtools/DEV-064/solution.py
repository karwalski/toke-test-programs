import sys
import json

def decode_vlq(encoded):
    """Decode a VLQ (Variable Length Quantity) encoded string."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = []
    i = 0
    
    while i < len(encoded):
        vlq = 0
        shift = 0
        continuation = True
        
        while continuation and i < len(encoded):
            char = encoded[i]
            i += 1
            digit = chars.index(char)
            continuation = (digit & 32) != 0
            digit &= 31
            vlq |= digit << shift
            shift += 5
        
        # Convert from unsigned to signed
        if vlq & 1:
            vlq = -(vlq >> 1)
        else:
            vlq = vlq >> 1
            
        result.append(vlq)
    
    return result

def parse_mappings(mappings):
    """Parse the mappings string and return segment information."""
    segments = []
    lines = mappings.split(';')
    
    # State for relative positions
    gen_col = 0
    source_idx = 0
    orig_line = 0
    orig_col = 0
    
    for line_idx, line in enumerate(lines):
        gen_col = 0  # Reset column for each line
        
        if not line:
            continue
            
        segs = line.split(',')
        for seg in segs:
            if not seg:
                continue
                
            decoded = decode_vlq(seg)
            if len(decoded) < 4:
                continue
                
            # Update relative positions
            gen_col += decoded[0]
            source_idx += decoded[1]
            orig_line += decoded[2]
            orig_col += decoded[3]
            
            segments.append({
                'gen_line': line_idx,
                'gen_col': gen_col,
                'source_idx': source_idx,
                'orig_line': orig_line,
                'orig_col': orig_col
            })
    
    return segments

def find_mapping(segments, target_line, target_col):
    """Find the best mapping for the given position."""
    best_match = None
    
    for seg in segments:
        if (seg['gen_line'] < target_line or 
            (seg['gen_line'] == target_line and seg['gen_col'] <= target_col)):
            if (best_match is None or 
                seg['gen_line'] > best_match['gen_line'] or
                (seg['gen_line'] == best_match['gen_line'] and 
                 seg['gen_col'] > best_match['gen_col'])):
                best_match = seg
    
    return best_match

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

position = lines[0]
source_map = json.loads(lines[1])

# Parse position (convert to 0-based)
line_col = position.split(':')
target_line = int(line_col[0]) - 1
target_col = int(line_col[1])

# Parse source map
mappings = source_map['mappings']
sources = source_map['sources']

# Decode mappings
segments = parse_mappings(mappings)

# Find the mapping
mapping = find_mapping(segments, target_line, target_col)

if mapping:
    source_file = sources[mapping['source_idx']]
    orig_line = mapping['orig_line'] + 1  # Convert back to 1-based
    orig_col = mapping['orig_col']
    print(f"original: {source_file}:{orig_line}:{orig_col}")
else:
    print("original: ::")