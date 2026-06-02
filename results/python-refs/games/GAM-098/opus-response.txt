# Try to figure out the rule from test cases:
# Test 1: RGBY -> RGBYRBY (added R, B, Y at positions 4,5,6)
# Test 2: R -> RRBYG (added R, B, Y, G at positions 1,2,3,4)
#
# Test 2 pos 1: prev=R(0), result=R(0). hash(prev)+pos mod 4 = 0+1=1? no, got 0
#   Maybe (prev + pos) mod 4: 0+1=1 -> G, but got R
#   Maybe (prev_ord + pos) mod 4: ord('R')=82, 82+1=83, 83%4=3 -> Y, no
#   pos starting 0: 0+0=0 -> R ✓
# Test 2 pos 2: prev=R(0), pos=1: 0+1=1 -> G, but got B
# Hmm. Let me try: prev is last char of sequence, mapping R=0,G=1,B=2,Y=3
# Test 2: R, then add R,B,Y,G
#   step 0: prev=R=0, pos=0: result R=0. (0+0)%4=0 ✓
#   step 1: prev=R=0, pos=1: result B=2. (0+1)=1 not 2
#   Maybe position is len: len=1, (0+1)%4=1=G, no
#   Maybe (prev + pos)*something
# Test 1: RGBY -> add R,B,Y
#   step 0: prev=Y=3, result R=0. 
#   step 1: prev=R=0, result B=2.
#   step 2: prev=B=2, result Y=3.
# Test 2: R -> add R,B,Y,G
#   step 0: prev=R=0, result R=0
#   step 1: prev=R=0, result B=2
#   step 2: prev=B=2, result Y=3
#   step 3: prev=Y=3, result G=1
# 
# Pattern of (prev, result): (3,0),(0,2),(2,3) and (0,0),(0,2),(2,3),(3,1)
# step uses position i (0-indexed in new additions)?
# Test1 step0: prev=3,i=0 -> 0. (3+0)%4=3, no. (3*?+0)
# Test2 step0: prev=0,i=0 -> 0. 
# Test1 step1: prev=0,i=1 -> 2
# Test2 step1: prev=0,i=1 -> 2  ✓ same
# Test1 step2: prev=2,i=2 -> 3
# Test2 step2: prev=2,i=2 -> 3  ✓ same
# Test2 step3: prev=3,i=3 -> 1
# Test1 step0: prev=3,i=0 -> 0. But test2 with prev=0,i=0 -> 0. So result doesn't depend on prev?
# Sequence of results by i: i=0->0(R), i=1->2(B), i=2->3(Y), i=3->1(G)
# That's just R,B,Y,G regardless of prev!
# 
# Check test1: i=0,1,2 -> R,B,Y ✓ (RGBY + RBY = RGBYRBY ✓)
# Check test2: i=0,1,2,3 -> R,B,Y,G ✓ (R + RBYG = RRBYG ✓)

s = input().strip().split()
seq = s[0]
n = int(s[1])
pattern = "RBYG"
for i in range(n):
    seq += pattern[i % 4]
print(seq)