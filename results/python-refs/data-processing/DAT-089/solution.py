import sys

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        return None
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def jaro_distance(s1, s2):
    if s1 == s2:
        return 1.0
    
    len_s1, len_s2 = len(s1), len(s2)
    
    if len_s1 == 0 or len_s2 == 0:
        return 0.0
    
    match_window = max(len_s1, len_s2) // 2 - 1
    if match_window < 0:
        match_window = 0
    
    s1_matches = [False] * len_s1
    s2_matches = [False] * len_s2
    
    matches = 0
    transpositions = 0
    
    # Find matches
    for i in range(len_s1):
        start = max(0, i - match_window)
        end = min(i + match_window + 1, len_s2)
        
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break
    
    if matches == 0:
        return 0.0
    
    # Find transpositions
    k = 0
    for i in range(len_s1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    
    jaro = (matches / len_s1 + matches / len_s2 + (matches - transpositions / 2) / matches) / 3
    return jaro

def jaro_winkler_distance(s1, s2):
    jaro = jaro_distance(s1, s2)
    
    if jaro < 0.7:
        return jaro
    
    # Find common prefix length (up to 4 characters)
    prefix = 0
    for i in range(min(len(s1), len(s2), 4)):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break
    
    return jaro + 0.1 * prefix * (1 - jaro)

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split(' ', 1)
        if len(parts) != 2:
            continue
        
        s1, s2 = parts
        
        lev = levenshtein_distance(s1, s2)
        ham = hamming_distance(s1, s2)
        jw = jaro_winkler_distance(s1, s2)
        
        ham_str = str(ham) if ham is not None else "-"
        
        print(f"{s1} {s2}\t{lev}\t{ham_str}\t{jw:.4f}")

if __name__ == "__main__":
    main()