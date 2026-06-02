import json
import sys
import re

def clean(s):
    s = s.strip()
    s = re.sub(r'^(however|but|although|though|nevertheless|on the other hand|and|or|so)[\s,]+', '', s, flags=re.IGNORECASE)
    s = re.sub(r'^(it|they|this|that|these|those)\s+', '', s, flags=re.IGNORECASE)
    return s.strip(' ,.')

def extract(text, topic):
    negative_indicators = ['reduce', 'reduces', 'decrease', 'decreases', 'harm', 'harms', 'hurt', 'hurts', 'damage', 'damages', 'worsen', 'worsens', 'cost', 'costs']
    
    contrast_pattern = re.compile(r'\s+(however|but|on the other hand)\s*,?\s*', re.IGNORECASE)
    
    pieces = []
    last_end = 0
    last_contrast = None
    for m in contrast_pattern.finditer(text):
        seg = text[last_end:m.start()]
        pieces.append((seg, last_contrast))
        last_contrast = m.group(1).lower()
        last_end = m.end()
    pieces.append((text[last_end:], last_contrast))
    
    final = []
    for seg, contrast in pieces:
        sents = re.split(r'[.!?]+', seg)
        first = True
        for s in sents:
            s = s.strip()
            if not s:
                continue
            final.append((s, contrast if first else None))
            first = False
    
    args_for = []
    args_against = []
    
    for sentence, contrast in final:
        # Split on as/since/because/averaging for claim+evidence
        m = re.split(r'\s+(?:as|since|because|averaging)\s+', sentence, maxsplit=1, flags=re.IGNORECASE)
        if len(m) == 2:
            # Determine separator used
            sep_match = re.search(r'\s+(as|since|because|averaging)\s+', sentence, flags=re.IGNORECASE)
            sep = sep_match.group(1).lower() if sep_match else ''
            claim = clean(m[0])
            if sep == 'averaging':
                evidence = clean('averaging ' + m[1])
            else:
                evidence = clean(m[1])
        else:
            claim = clean(sentence)
            evidence = None
        
        claim = re.sub(rf'^{re.escape(topic)}\s+', '', claim, flags=re.IGNORECASE).strip()
        # Also try removing "but" prefix from claim
        claim = re.sub(r'^but\s+', '', claim, flags=re.IGNORECASE).strip()
        
        if not claim:
            continue
        
        is_negative = any(re.search(rf'\b{ind}\b', claim.lower()) for ind in negative_indicators)
        
        if contrast in ('however',) or (contrast == 'but'):
            if is_negative:
                args_against.append({"claim": claim, "evidence": evidence})
            else:
                args_for.append({"claim": claim, "evidence": evidence})
        else:
            if is_negative:
                # Check if "but" is in original sentence preceding this claim - handled differently
                args_against.append({"claim": claim, "evidence": evidence})
            else:
                args_for.append({"claim": claim, "evidence": evidence})
    
    # Handle sentence-internal "but" splits
    # Re-process: for sentences containing " but " split them
    args_for2 = []
    args_against2 = []
    for a in args_for:
        c = a['claim']
        if ' but ' in c.lower():
            parts = re.split(r'\s+but\s+', c, maxsplit=1, flags=re.IGNORECASE)
            first_claim = parts[0].strip()
            second_claim = parts[1].strip()
            # First part stays positive
            is_neg1 = any(re.search(rf'\b{ind}\b', first_claim.lower()) for ind in negative_indicators)
            is_neg2 = any(re.search(rf'\b{ind}\b', second_claim.lower()) for ind in negative_indicators)
            if is_neg1:
                args_against2.append({"claim": first_claim, "evidence": a['evidence']})
            else:
                args_for2.append({"claim": first_claim, "evidence": a['evidence']})
            args_against2.append({"claim": second_claim, "evidence": None})
        else:
            args_for2.append(a)
    
    args_for = args_for2
    args_against = args_against + args_against2
    
    seen = set()
    uf = []
    for a in args_for:
        if a['claim'] not in seen:
            seen.add(a['claim'])
            uf.append(a)
    seen = set()
    ua = []
    for a in args_against:
        if a['claim'] not in seen:
            seen.add(a['claim'])
            ua.append(a)
    
    return uf, ua

def main():
    data = json.loads(sys.stdin.read())
    text = data['text']
    topic = data['topic']
    af, ag = extract(text, topic)
    output = {"arguments_for": af, "arguments_against": ag}
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()