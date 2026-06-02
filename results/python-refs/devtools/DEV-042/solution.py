import sys

def parse_input(data):
    lines = data.split('\n')
    if not lines:
        return 0, {}
    min_lines = int(lines[0].strip())
    files = {}
    current = None
    buf = []
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.startswith('---FILE:') and line.rstrip().endswith('---'):
            if current is not None:
                files[current] = buf
            current = line[len('---FILE:'):-3].strip()
            buf = []
        else:
            if current is not None:
                buf.append(line)
        i += 1
    if current is not None:
        # strip trailing empty line artifact from final newline split
        files[current] = buf
    return min_lines, files

def is_meaningful(line):
    s = line.strip()
    if not s:
        return False
    if s.startswith('#'):
        return False
    return True

def extract_meaningful(file_lines):
    # returns list of (original_line_number_1based, stripped_content)
    result = []
    for idx, ln in enumerate(file_lines, start=1):
        if is_meaningful(ln):
            result.append((idx, ln.strip()))
    return result

def find_duplicates(min_lines, files):
    # files: name -> list of original lines
    meaningful = {name: extract_meaningful(lines) for name, lines in files.items()}
    # Build all blocks of size >= min_lines from each file (using meaningful lines)
    # block keyed by tuple of content lines; value list of (file, start_line_number_in_original)
    blocks = {}
    file_names = sorted(meaningful.keys())
    for fname in file_names:
        m = meaningful[fname]
        n = len(m)
        if n < min_lines:
            continue
        for i in range(n - min_lines + 1):
            # try maximal blocks: for each starting position, only record block of exactly min_lines
            # but to find longest, we'll iterate sizes from min_lines up to n-i
            for size in range(min_lines, n - i + 1):
                segment = tuple(c for _, c in m[i:i+size])
                start_orig = m[i][0]
                blocks.setdefault(segment, []).append((fname, start_orig, size))
    # Find duplicate segments: appearing in 2+ locations (across files or same file different positions)
    # Keep only maximal: a block is maximal if extending it (by one line on either side) breaks the duplication count
    # Simpler approach: find all segments with >=2 occurrences, then filter out those contained in a larger duplicate segment with same occurrence set.
    dup_segments = {seg: locs for seg, locs in blocks.items() if len(locs) >= 2}
    # Build occurrence signature per segment
    # Filter: keep segment if no longer segment exists whose occurrences cover this segment's occurrences
    seg_list = list(dup_segments.keys())
    # Sort by length desc
    seg_list.sort(key=lambda s: -len(s))
    kept = []
    used_ranges = []  # list of sets of (file,start,end)
    for seg in seg_list:
        locs = dup_segments[seg]
        size = len(seg)
        # ranges in terms of meaningful index? we stored original line. We need meaningful indices to test containment.
        # Recompute meaningful index for each loc
        cur_ranges = set()
        for fname, start_orig, sz in locs:
            m = meaningful[fname]
            # find index of start_orig in m
            for idx, (oln, _) in enumerate(m):
                if oln == start_orig:
                    cur_ranges.add((fname, idx, idx + sz - 1))
                    break
        # check if any kept range fully contains all of cur_ranges
        contained = False
        for kr in used_ranges:
            # cur_ranges contained if every range in cur_ranges is inside some range in kr
            ok = True
            for (fn, a, b) in cur_ranges:
                found = False
                for (fn2, a2, b2) in kr:
                    if fn == fn2 and a2 <= a and b <= b2:
                        found = True
                        break
                if not found:
                    ok = False
                    break
            if ok:
                contained = True
                break
        if not contained:
            kept.append((seg, locs, size))
            used_ranges.append(cur_ranges)
    return kept

def main():
    data = sys.stdin.read()
    min_lines, files = parse_input(data)
    dups = find_duplicates(min_lines, files)
    if not dups:
        print('No duplicates found')
        return
    # Sort output for determinism: by size desc, then by first file/line
    dups.sort(key=lambda x: (-x[2], sorted(x[1])))
    out_lines = []
    for seg, locs, size in dups:
        out_lines.append('Duplicate block ({} lines):'.format(size))
        for fname, start_orig, sz in sorted(locs):
            out_lines.append('  {}:{}'.format(fname, start_orig))
    print('\n'.join(out_lines))

main()
