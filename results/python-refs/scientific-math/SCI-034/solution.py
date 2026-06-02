import sys

def compute_lps(p):
    lps=[0]*len(p)
    k=0
    for i in range(1,len(p)):
        while k>0 and p[k]!=p[i]:
            k=lps[k-1]
        if p[k]==p[i]:
            k+=1
        lps[i]=k
    return lps

def kmp(text,pat):
    positions=[]
    comparisons=0
    if not pat:
        return positions,0,[]
    lps=compute_lps(pat)
    n=len(text); m=len(pat)
    i=0; j=0
    while i<n:
        comparisons+=1
        if text[i]==pat[j]:
            i+=1; j+=1
            if j==m:
                positions.append(i-j)
                j=lps[j-1]
        else:
            if j!=0:
                j=lps[j-1]
            else:
                i+=1
    return positions,comparisons,lps

data=sys.stdin.read().split('\n')
pat=data[0] if len(data)>0 else ''
text=data[1] if len(data)>1 else ''
positions,comparisons,lps=kmp(text,pat)
if positions:
    print('Found at positions: '+' '.join(str(x) for x in positions))
else:
    print('NOT FOUND')
print('Comparisons: '+str(comparisons))
