Looking at test 1 expected:
- chunk 0: 0-20 "The quick brown fox "
- chunk 1: 15-35 "fox jumps over the l" — wait, text[15:35]?

Let me check: "The quick brown fox jumps over the lazy dog near the river bank"
Positions: T(0)h(1)e(2) (3)q(4)u(5)i(6)c(7)k(8) (9)b(10)r(11)o(12)w(13)n(14) (15)f(16)o(17)x(18) (19)j(20)...

text[15:35] = " fox jumps over the " but expected is "fox jumps over the l" which is text[16:36].

Test 1 text length: let me count. "The quick brown fox jumps over the lazy dog near the river bank" - expected last chunk end_offset=65 but text is 63 chars... so end_offset goes beyond text length?

Wait, expected end_offset=50 for chunk 2, text "he lazy dog near the" which is 20 chars. So start would be 30. text[30:50]... let me recount.

"The quick brown fox jumps over the lazy dog near the river bank"
T-h-e- -q-u-i-c-k- -b-r-o-w-n- -f-o-x- -j-u-m-p-s- -o-v-e-r- -t-h-e- -l-a-z-y- -d-o-g- -n-e-a-r- -t-h-e- -r-i-v-e-r- -b-a-n-k
0123456789...

Length = 63. But end_offset=65 in last chunk. Strange.

Chunk 1: start=15, "fox jumps over the l". Position 15 is ' ', 16 is 'f'. So expected text starts at 16, but start_offset says 15. Hmm.

Maybe they strip leading space? Chunk 1 raw text[15:35]=" fox jumps over the ", stripped left = "fox jumps over the " (19 chars). Not matching "fox jumps over the l" (20 chars).

Maybe chunks skip leading whitespace by advancing start but keep original start_offset, then extend end by same amount? text[16:36] = "fox jumps over the l" ✓. start_offset=15, end_offset=35 reported but actual slice is [16:36].

Chunk 2: expected "he lazy dog near the", start_offset=30, end_offset=50. Position 30=' ', 31='t', 32='h', 33='e'... so text[30:50]=" the lazy dog near t". Skip 2 leading? text[32:52]="he lazy dog near the" ✓ (20 chars). start_offset=30, end=50 reported.

So it seems: strip leading spaces, shift the window forward by the stripped count, but report original offsets? Hmm but chunk 1 shifted by 1, chunk 2 by 2.

Chunk 3: start_offset=49, end_offset=65. Previous end_offset=50, overlap=5, next start = 50-5=45. text[45]='r',46='e',47='r',48=' ',49='t'... Hmm expected "r the river bank". text[45:65]="r the river bank" - let's count: r(45)-(46) wait let me recount carefully.

"The quick brown fox jumps over the lazy dog near the river bank"
 0123456789012345678901234567890123456789012345678901234567890123
 0         1         2         3         4         5         6

T=0,h=1,e=2,' '=3,q=4,u=5,i=6,c=7,k=8,' '=9,b=10,r=11,o=12,w=13,n=14,' '=15,f=16,o=17,x=18,' '=19,j=20,u=21,m=22,p=23,s=24,' '=25,o=26,v=27,e=28,r=29,' '=30,t=31,h=32,e=33,' '=34,l=35,a=36,z=37,y=38,' '=39,d=40,o=41,g=42,' '=43,n=44,e=45,a=46,r=47,' '=48,t=49,h=50,e=51,' '=52,r=53,i=54,v=55,e=56,r=57,' '=58,b=59,a=60,n=61,k=62

Length=63. text[49:65]="the river bank" (only 14 chars since length 63). Expected "r the river bank" is 16 chars.

Hmm. text[47:63]="r the river bank" ✓ (r=47,' '=48,t=49,h=50,e=51,' '=52,r=53,i=54,v=55,e=56,r=57,' '=58,b=59,a=60,n=61,k=62) — that's 16 chars ✓.

But start_offset=49, end_offset=65. Neither matches [47:63]. So offsets are NOT the actual text positions.

Let me look at the pattern of offsets:
- Chunk 0: start=0, end=20
- Chunk 1: start=15, end=35 (diff from prev: 15=20-5 overlap)
- Chunk 2: start=30, end=50
- Chunk 3: start=49, end=65 (diff: 50-49=1, not 5)

So start positions follow chunk_size-overlap=15 stride normally: 0,15,30,45. But chunk 3 says 49. Hmm.

Actually maybe the algorithm finds word boundaries. Let's see:
- Chunk 0 text "The quick brown fox " ends at position 20 (after space)
- Chunk 1 text "fox jumps over the l" - starts mid... actually starts at "fox" which is at position 16. 

Maybe: the start_offset is computed assuming uniform stride, but the actual text starts at nearest word boundary?

Pattern: nominal_start = i*(chunk_size-overlap). For i=0,1,2,3: 0,15,30,45.
But chunk 3 start=49, not 45. And end=65 not 63 (text len).

Maybe they look for next space after nominal start? At position 15 there's a space - so skip past it: actual=16. But start_offset reported=15. Hmm.

Or maybe text is treated as space-separated words and we chunk by words? Let me check chunk lengths:
- "The quick brown fox " = 20 chars ending with space
- "fox jumps over the l" = 20 chars  
- "he lazy dog near the" = 20 chars
- "r the river bank" = 16 chars

These aren't word-aligned. 

Let me look again: maybe start_offset and end_offset are NOT actual string offsets but cumulative-style counters?

stride = chunk_size - overlap = 15. 
- chunk 0: start=0, text=text[0:20]
- chunk 1: start=15 (=stride*1), text should be text[?:?]
- chunk 2: start=30 (=stride*2)
- chunk 3: ??? expected 49

Hmm. Let's think differently. What if start_offset increases by stride normally but the LAST chunk uses end-chunk_size? Like right-align last chunk?

Actually 65-16=49. So if last chunk is 16 chars and end=65, start=49. And 65 = ? Text length is 63. Maybe end_offset is computed as start + (some intended size)?

Wait, what if there's a different stride? After chunk 2 (start=30, end=50), next start using overlap of 5 from end: 50-5=45. text[45:65] but text only has 63 chars. text[45:63]="eaar the river bank"? Let me recount: 45=e,46=a,47=r,48=' ',49=t,50=h,51=e,52=' ',53=r,54=i,55=v,56=e,57=r,58=' ',59=b,60=a,61=n,62=k. So text[45:63]="ear the river bank" (18 chars). Not matching "r the river bank" (16 chars).

text[47:63]="r the river bank" ✓. So actual start is 47, but reported as 49? 

Wait! Maybe the spec is buggy and the test expectations are weird. Let me look at chunk 1 again. start_offset=15, but actual text shown corresponds to text[16:36]. Could the algorithm be: strip the chunk and adjust offsets?

" fox jumps over the ".lstrip() = "fox jumps over the " (19 chars). Not 20.

What if both lstrip and pad? Take stride positions 15,30,45 raw text, but the displayed text is text[start+1:start+1+chunk_size] if there's a leading space?

- Chunk 1: start=15, text[16:36]="fox jumps over the l" ✓, end=35 reported (=15+20)
- Chunk 2: start=30, text[30]=' ', so text[31:51]? text[31:51]="the lazy dog near th". Expected "he lazy dog near the". That's text[32:52]. So shifted by 2.

Hmm so shift varies. text[30]=' ', text[31]='t'. If we skip space, shift=1: text[31:51]="the lazy dog near th". But expected is "he lazy dog near the" = text[32:52]. Shift=2.

That's weird. Unless... overlap of words?

Let me try: maybe shift = (previous chunk ending). Chunk 1's text ends at "...the l" so position 36. Next chunk at 36-overlap=31? No 36-5=31. But shift was 2 (position 32).

Let me try a completely different interpretation: maybe these are chunks based on character positions but with sentence/word adjustment to land on certain boundaries. The example seems to favor chunks NOT starting with spaces.

Chunk 1 text "fox jumps over the l" - doesn't start with space ✓
Chunk 2 text "he lazy dog near the" - doesn't start with space ✓
Chunk 3 text "r the river bank" - doesn't start with space ✓

And no chunk starts with space. Also chunks 1,2,3 don't end the same way.

What if the algorithm is: start = previous_end - overlap, then if text[start] is space, advance? But:
- After chunk 0 (end=20): start=15, text[15]=' ', advance to 16. But reported start_offset=15.
- After chunk 1 (end=35): start=30, text[30]=' ', advance to 31. text[31]='t', not 'h'. But chunk2 starts with 'h'.

Hmm.

Let me check: maybe end_offset doesn't equal start+chunk_size and chunks aren't aligned to fixed stride.

Chunk 0: start=0, end=20, len=20
Chunk 1: start=15, end=35, len=20  
Chunk 2: start=30, end=50, len=20
Chunk 3: start=49, end=65, len=16

Actual text length of each chunk:
- "The quick brown fox " = 20
- "fox jumps over the l" = 20
- "he lazy dog near the" = 20
- "r the river bank" = 16

So lengths match end-start. Good.

Now for chunk 1: start_offset=15, len 20, but text[15:35]=" fox jumps over the ". The actual displayed text "fox jumps over the l" is text[16:36]. So offsets are off by 1!

Chunk 2: start_offset=30, len 20, but displayed text[32:52]. Off by 2!

Chunk 3: start_offset=49, len 16, displayed text[47:63]. Off by -2!

Hmm strange. Or maybe I'm miscounting the text. Let me recount the original text super carefully.

"The quick brown fox jumps over the lazy dog near the river bank"

Splitting: "The"(3) " "(1) "quick"(5) " "(1) "brown"(5) " "(1) "fox"(3) " "(1) "jumps"(5) " "(1) "over"(4) " "(1) "the"(3) " "(1) "lazy"(4) " "(1) "dog"(3) " "(1) "near"(4) " "(1) "the"(3) " "(1) "river"(5) " "(1) "bank"(4)

Total = 3+1+5+1+5+1+3+1+5+1+4+1+3+1+4+1+3+1+4+1+3+1+5+1+4 = 63. Confirmed.

Hmm I wonder if the test expected output is just incorrect/inconsistent. But we need to match it.

Let me try