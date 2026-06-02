Let me verify test 1: income=80000, brackets: (18200, 0), (45000, 0.19), (120000, 0.325)
- 0-18200: 0% = 0
- 18200-45000: 19% on 26800 = 5092
- 45000-80000: 32.5% on 35000 = 11375
Total = 16467... but expected is 14617.

Hmm. Let me reconsider. The "threshold rate" means income above this threshold is taxed at this rate up to next threshold. So:
- 0-18200: rate 0 → 0
- 18200-45000: rate from first bracket, which says threshold 18200 rate 0... 

Wait, maybe rate listed is for income below that threshold (up to it)? 
- up to 18200 at 0%: 0
- 18200-45000 at 0.19: 26800*0.19 = 5092
- 45000-120000 at 0.325: 35000*0.325 = 11375
Total 16467, still not 14617.

Expected 14617. Let me try: 14617/35000 = 0.4176. Try threshold rate means rate applies to amount above threshold incrementally?

Standard Australian: 18200-45000 @ 19%, 45000-120000 @ 32.5%. 
26800*0.19 + 35000*0.325 = 5092 + 11375 = 16467.

But expected 14617 = 16467 - 1850. Hmm.

Try: rate is the rate for that bracket (above threshold). So threshold 18200 rate 0 means above 18200 rate 0? No.

Try: 80000 * something. 14617/80000 = 0.1827.

Test 2: 50000, brackets (10000,0),(40000,0.20),(100000,0.30). Expected 9000.
- 10000-40000 @ 0.20 = 6000, 40000-50000 @ 0.30 = 3000, total = 9000. ✓

So test 2 uses: each bracket (threshold, rate) means from this threshold to next, rate applies. Apply this to test 1:
- 18200-45000 @ 0 = 0
- 45000-80000 @ 0.19 = 6650
Total = 6650. That's what current code outputs! But expected 14617.

Wait, test 1 expected 14617. Let me check: 14617 = ?
45000-80000 at some rate plus more? 35000*0.325 = 11375, + 3242? 
18200-45000 at 0.19 = 5092, + 80000-? 14617-5092=9525, 9525/0.325=29307. Hmm.

Maybe: rate listed with threshold means rate above that threshold:
- above 18200 at 0% — no that gives 0
- Actually let me try threshold=upper bound:
  - 0-18200 @ 0 = 0
  - 18200-45000 @ 0.19 = 26800*0.19=5092
  - 45000-120000 @ 0.325, but capped at 80000: 35000*0.325=11375
  - Total 16467

14617 vs 16467 diff = 1850 = 18200*0.1017... or 5092 - something.

Let me try: rate associated with threshold applies starting at threshold:
- threshold 18200 rate 0: from 18200 onwards at 0 until 45000
- threshold 45000 rate 0.19: from 45000 onwards at 0.19 until 120000  
- threshold 120000 rate 0.325: from 120000 onwards

Test 1: 80000. 
- 0-18200: untaxed
- 18200-45000 @ 0: 0
- 45000-80000 @ 0.19: 35000*0.19 = 6650
Total 6650. Not 14617.

Test 2 with this interpretation:
- 0-10000: untaxed
- 10000-40000 @ 0: 0
- 40000-50000 @ 0.20: 10000*0.20 = 2000
Not 9000.

So test 2's interpretation: rate at threshold N applies UP TO threshold N (or from previous to N).

Test 2 working interpretation: bracket (T, R) means rate R applies from previous threshold up to T. Last bracket extends beyond.
- (10000, 0): 0-10000 @ 0 = 0
- (40000, 0.20): 10000-40000 @ 0.20 = 6000
- (100000, 0.30): 40000-100000 @ 0.30, capped at 50000: 10000*0.30 = 3000
Total 9000 ✓

Test 1 with this:
- (18200, 0): 0-18200 @ 0 = 0
- (45000, 0.19): 18200-45000 @ 0.19 = 5092
- (120000, 0.325): 45000-120000 @ 0.325, capped at 80000: 35000*0.325 = 11375
Total 16467 ≠ 14617.

Hmm. So inconsistent. 14617... Australian tax for 80000: actually Australia 2020: 18201-45000 @ 19%, 45001-120000 @ 32.5%, gives 5092+11375=16467. Medicare levy 2% = 1600. Total ~18067. Not 14617.

Let me check: 14617 = 5092 + 9525. 9525 = ?  35000 * 0.272 = 9520. Or 80000*0.325 - 11383?

Actually: 80000 * 0.325 = 26000 - 14617 = 11383. Hmm, LITO?

Or simpler: 14617 = ? Let me try other arrangement. What if rate is for income at/below threshold for that whole bracket?
- 80000 falls in 120000 bracket @ 0.325. 80000 * 0.325 = 26000. No.
- (80000-18200) * something? 61800 * 0.2365 ≈ 14617. 14617/61800 = 0.2365. 

Or maybe: brackets are (lower threshold, rate applying above):
- 18200, 0: above 18200, rate 0 (until next)
- 45000, 0.19: above 45000, rate 0.19 (until next)
- 120000, 0.325: above 120000

Test 1: 80000:
- 18200-45000 @ 0 = 0
- 45000-80000 @ 0.19 = 6650
That's 6650 ≠ 14617.

Hmm I'm stuck on test 1's expected. Let me verify by computing 14617 more carefully.

What if it's compounding/cumulative? 

Actually let me try: each bracket's threshold is "tax at full" plus marginal. Like Australia: at 45000 you owe 5092, plus 32.5% over 45000. 80000-45000=35000. 35000*0.325 = 11375. 11375+5092 = 16467. Still not 14617.

14617/35000 = 0.4176. (80000-?) * rate.

What if the rate for each bracket is total marginal rate but only difference applied incrementally?
Bracket rates as differences: 0, 0.19, 0.325 (already cumulative-marginal).

Try: apply rate to (income - threshold) for each bracket where income > threshold, summing:
- income > 18200: (80000-18200)*0 = 0
- income > 45000: (80000-45000)*0.19 = 6650
- income > 120000: no
Total 6650. Same.

Try summing all such with full rate:
- (80000-18200)*0 + (80000-45000)*0.19 = 0 + 6650 = 6650. No.

Try (threshold)*rate:
- 18200*0 + 45000*0.19 + 120000*0.325 — caps?

What about cumulative from top? Income 80000, top applicable bracket (45000, 0.19). 80000*0.19 = 15200. - 18200*0.19=3458, = 11742. No.

14617 ... Let me try: 80000 * 0.19 = 15200 - 583 = 14617. 583 = 18200*0.032? 

Or 14617 = 80000*0.19 - 18200*0.032... random.

Let me try yet another: tax = sum over brackets of max(0, income - threshold) * rate:
- max(0, 80000-18200)*0 = 0
- max(0, 80000-45000)*0.19 = 6650
- max(0, 80000-120000)*0.325 = 0
Total 6650.

Test 2: max(0,50000-10000)*0 + max(0,50000-40000)*0.20 + max(0,50000-100000)*0.30 = 0 + 2000 + 0 = 2000. Not 9000.

So test 2 doesn't use that interpretation either.

Given the inconsistency, test 2 expects 9000 with interpretation A (threshold = upper of bracket), test 1 expects 14617 which doesn't match interpretation A (gives 16467).

Wait—maybe I miscalculated. Let me redo test 1 interp A carefully:
- Bracket 1: (18200, 0). Income from 0 to 18200, rate 0%. Tax = 18200*0 = 0.
- Bracket 2: (45000, 0.19). Income from 18200 to 45000, rate 19%. Tax = (45000-18200)*0.19 = 26800*0.19 = 5092.
- Bracket 3: (120000, 0.325). Income from 45000 to 120000, rate 32.5%. Income capped at 80000. Tax = (80000-45000)*0.325 = 35000*0.325 = 11375.
Total = 0 + 5092 + 11375 = 16467.

Expected 14617. Diff = 1850. Hmm 1850 = ? 18200 * 0.1017 or...

Oh wait! What if "income below first threshold is tax-free" means we subtract first threshold from income before applying brackets??

Test 1: effective income = 80000 - 18200 = 61800.
- (18200, 0): not used as bracket, just exemption
- (45000, 0.19): applied to first portion of 61800. Up to 45000-18200=26800 at 0.19 = 5092
- (120000, 0.325): remaining 61800-26800 = 35000 at 0.325 = 11375
Total 16467. Same answer.

Hmm. Or maybe rates work differently. 14617... let me check if this is "tax + medicare - LITO". Or tax calculator with LITO (low income tax offset). For 80000 Australian: LITO around 700-1080. Doesn't match.

OK let me search 14617 specifically. Could the answer simply be wrong in the spec? Or perhaps the formula is something else entirely.

Try: bracket(T,R) means rate R applies above T. Treat brackets as marginal rates from T to next T:
- Above 18200, until 45000: rate 0. 0.
- Above 45000, until 120000: rate 0.19. (80000-45000)*0.19 = 6650
- Above 120000: 0.325. 0.
Total 6650. Test 2: above 10000 to 40000 rate 0=0; above 40000 to 100000 rate 0.20: (50000-40000)*0.20=2000. Not 9000.

So that doesn't work for test 2.

What if each bracket has rate that's a TOTAL rate up to that threshold, and excess uses next rate?
Test 2: bracket(40000, 0.20): up to 40000, total tax = 40000*0.20 = 8000. Then 50000-40000=10000 at 0.30 = 3000. Total 11000. Not 9000.

What if bracket = (threshold-where-rate-starts, rate):
Test 2: 
- (10000, 0): from 10000 onwards rate 0
- (40000, 0.20): from 40000 onwards 0.20
- (100000, 0.30): from 100000 onwards 0.30
Income 50000: 
- 0-10000: tax-free (below first)
- 10000-40000 @ 0 = 0
- 40000-50000 @ 0.20 = 2000
Total 2000. Not 9000.

For test 2 to give 9000, must be: bracket(T,R) means rate R from previous-T to current-T. That's interpretation A.

Hmm, looking again at test 1 with interp A: 16467. But expected 14617. Difference is exactly 1850.

Wait... 1850 = (18200 - 0) * something? Or what if FIRST bracket means r