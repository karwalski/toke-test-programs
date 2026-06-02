import json
import sys
import re
from difflib import SequenceMatcher

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    stopwords = {'a','an','the','is','are','was','were','do','does','did','how','what','when','where','why','who','can','could','should','would','will','i','you','my','your','to','of','in','on','for','and','or','but'}
    return [t for t in tokens if t not in stopwords]

SYNONYMS = [
    {'reset','change','modify','update','alter'},
    {'password','passcode','pwd'},
]

def normalize_token(tok):
    for group in SYNONYMS:
        if tok in group:
            return min(group)
    return tok

def similarity(a, b):
    ta = [normalize_token(t) for t in preprocess(a)]
    tb = [normalize_token(t) for t in preprocess(b)]
    if not ta or not tb:
        return 0.0
    sa, sb = set(ta), set(tb)
    jaccard = len(sa & sb) / len(sa | sb)
    seq = SequenceMatcher(None, ' '.join(ta), ' '.join(tb)).ratio()
    return max(jaccard, seq)

def main():
    data = json.loads(sys.stdin.read())
    new_item = data['new_item']
    existing = data['existing_items']
    
    best_sim = 0.0
    best_id = None
    for item in existing:
        s = similarity(new_item, item['text'])
        if s > best_sim:
            best_sim = s
            best_id = item['id']
    
    rounded = round(best_sim, 1)
    is_dup = rounded >= 0.8
    result = {
        "is_duplicate": is_dup,
        "duplicate_of": best_id if is_dup else None,
        "similarity": rounded
    }
    print(json.dumps(result, separators=(',', ':')))

main()