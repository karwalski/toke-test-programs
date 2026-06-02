Let me analyze test 1:
Sentences: "The cat sat on the mat.", "The dog barked loudly.", "The cat ran away.", "The dog was happy."

Word frequencies (lowercase):
- the: 2+1+2+1 = wait let me recount
- S1: the, cat, sat, on, the, mat → the=2, cat=1, sat=1, on=1, mat=1
- S2: the, dog, barked, loudly → the=1, dog=1, barked=1, loudly=1
- S3: the, cat, ran, away → the=1, cat=1, ran=1, away=1
- S4: the, dog, was, happy → the=1, dog=1, was=1, happy=1

Total: the=5, cat=2, dog=2, sat=1, on=1, mat=1, barked=1, loudly=1, ran=1, away=1, was=1, happy=1

Scores:
- S1: 5+2+1+1+5+1 = 15
- S2: 5+2+1+1 = 9
- S3: 5+2+1+1 = 9
- S4: 5+2+1+1 = 9

Expected top 3: S1, S3, S4. But ties give S1, S2, S3.

Maybe normalize by length? Or use average? Let's try average:
- S1: 15/6 = 2.5
- S2: 9/4 = 2.25
- S3: 9/4 = 2.25
- S4: 9/4 = 2.25

Still tied. Maybe tie-break by later order? Expected picks S1, S3, S4 — skipping S2. 

Maybe TF-IDF where "the" appears in all sentences gets IDF=0. With IDF = log(N/df):
- the: df=4, idf=log(4/4)=0
- cat: df=2, idf=log(4/2)=log(2)
- dog: df=2, idf=log(2)
- others: df=1, idf=log(4)

S1 score (sum tf*idf): the(2*0) + cat(1*log2) + sat(log4) + on(log4) + mat(log4) = log2 + 3*log4 = log2+6log2 = 7log2
S2: the(0) + dog(log2) + barked(log4) + loudly(log4) = log2+4log2 = 5log2
S3: the(0) + cat(log2) + ran(log4) + away(log4) = log2+4log2 = 5log2
S4: the(0) + dog(log2) + was(log4) + happy(log4) = 5log2

Still ties between S2, S3, S4. Expected picks S3, S4 over S2. Tie-break later in document?

If tie-break is reverse order (prefer later), then S4, S3 would beat S2. Top 3 = S1, S3, S4. ✓

```python
import sys
import re
from collections import Counter
import math

def main():
    data = sys.stdin.read()
    nl = data.find('\n')
    if nl == -1:
        n = int(data.strip())
        text = ''
    else:
        n = int(data[:nl].strip())
        text = data[nl+1:]
    
    parts = re.split(r'([.!?]+)', text)
    sentences = []
    for i in range(0, len(parts)-1, 2):
        body = parts[i].strip()
        delim = parts[i+1] if i+1 < len(parts) else ''
        if body:
            sentences.append(body + (delim[0] if delim else ''))
    if len(parts) % 2 == 1:
        tail = parts[-1].strip()
        if tail:
            sentences.append(tail)
    
    if not sentences:
        return
    
    tokenized = []
    df = Counter()
    for s in sentences:
        words = re.findall(r'\b\w+\b', s.lower())
        tokenized.append(words)
        for w in set(words):
            df[w] += 1
    
    N = len(sentences)
    scored = []
    for i, words in enumerate(tokenized):
        tf = Counter(words)
        score = sum(tf[w] * math.log(N/df[w]) for w in tf) if N > 1 else sum(tf.values())
        scored.append((score, -i, i))
    
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = sorted(scored[:n], key=lambda x: x[2])
    
    print('\n'.join(sentences[i] for _, _, i in top))

if __name__ == "__main__":
    main()
```