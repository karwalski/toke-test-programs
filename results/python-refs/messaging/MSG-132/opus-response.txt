I need to figure out the percentile interpolation method.

Test 1: latencies [50, 80, 200, 600]
- p50 = 140 = (80+200)/2 ... hmm, or linear interpolation
- p95 = 500
- p99 = 580

For n=4 sorted [50,80,200,600]:
- Linear interpolation method: rank = p/100 * (n-1)
  - p50: 0.5*3 = 1.5 → 80 + 0.5*(200-80) = 140 ✓
  - p95: 0.95*3 = 2.85 → 200 + 0.85*(600-200) = 200+340 = 540 ✗
  - With n+1: p95: 0.95*4 = 3.8... index 3 max
  - Try rank = p/100 * n: p95: 0.95*4 = 3.8, between index 3 and... only 4 elements
  - rank = p/100*(n+1) - 1: p95: 0.95*5-1 = 3.75 → past end
  
Let me try: p95 = 500. Between 200 and 600, 500 = 200 + 0.75*400. So fraction 0.75 at index 2→3.
- 0.75 = 0.95*n - 2? 0.95*4-2 = 1.8, no. 
- Maybe: index = (p/100)*(n-1), at 0.95*3=2.85 → 200+0.85*400=540. No.
- Try index from 1-based: rank = p/100*(n+1) = 0.95*5 = 4.75... 
- Try: p95: 0.95*4 -0.5= 3.3 → between idx 3 (=600)... no
- For p99=580: 580 = 200+0.95*400, so fraction 0.95 between 200 and 600
- For p95=500: fraction 0.75 between 200 and 600
- 0.95 corresponds to p99, 0.75 to p95... difference 0.20 per 4 points
- Linear: at p=50, fraction between which? p50=140, between 80(idx1) and 200(idx2), fraction 0.5
- So p=50 → idx 1.5; p=95 → idx 2.75; p=99 → idx 2.95
- 95: 2.75 = ? Try (p-5)/100 * (n-1) + ... 0.5→1.5, 0.95→2.75, 0.99→2.95
- Linear in p: idx = a*p + b. 50→1.5, 95→2.75: slope=1.25/45, b=1.5-50*1.25/45=1.5-1.389=0.111
- Check 99: 99*1.25/45+0.111 = 2.75+4*1.25/45 = 2.75+0.111 = 2.861. But we need 2.95. Doesn't match linear.

Try: idx = p/100 * n - 0.5: p50: 1.5 ✓, p95: 3.3, p99: 3.46. No.

Maybe p99 uses different. 580 = 80 + 500? Or weighted differently. Actually 580 = (200+600)*... no.
600-580=20, 580-200=380. 380/400 = 0.95. So p99 puts 99% weight on upper.
500-200=300, 600-500=100. 300/400 = 0.75. p95 puts 75% weight on upper.

For percentile p with n=4: weight on upper = ?
- p50: weight 0.5 between idx1,2
- p95: weight 0.75 between idx2,3
- p99: weight 0.95 between idx2,3

Hmm p95 and p99 both between idx2,3. Method: numpy 'lower'? No. 

Try `statistics.quantiles(data, n=100, method='inclusive')` - this uses (n-1) interpolation. p95 index 95th of 99 percentiles.

Actually `statistics.quantiles(data, n=100)` returns 99 values. The k-th (1-indexed) is the k/100 quantile. With method='exclusive' default: idx = k*(N+1)/100. For N=4: p95: 95*5/100=4.75, p99: 99*5/100=4.95. Both past end (max idx 3), would clamp to 600. No.

Method 'inclusive': idx = k*(N-1)/100. p95: 95*3/100=2.85, p99: 99*3/100=2.97.
- p95: 200+0.85*400=540 ✗
- p99: 200+0.97*400=588 ✗ (close to 580 but not exact)

Hmm. What if interpolation uses idx = p*(n-1)/100 but uses statistics module... Let me just compute statistics.quantiles output.

Actually wait — maybe percentiles computed differently. Let me try: `idx = p/100 * (n+1) - 1`: p50: 0.5*5-1=1.5 ✓, p95: 0.95*5-1=3.75 (past), p99: similar.

What gives 500 and 580 exactly? p95=500: between 200,600 fraction 0.75. p99=580 fraction 0.95.
Both between same indices. 0.75 and 0.95 — note 0.95 = (99-80)/20 if p95 at 80%, p100 at 100%? Linear: p95→0.75, p99→0.95, slope 0.05 per p, so p_x → 0.05*(x-80)+0.75? Check p95: 0.05*15+0.75=1.5. No.

Slope (0.95-0.75)/(99-95) = 0.05. p95→0.75 means at p=95, frac=0.75; extrapolate p=80→0. So formula: frac = (p-80)/20 for upper interp between idx2,idx3.

Why 80? n=4, maybe each element gets 25%. percentile p: idx = p/25 = floor part + frac. p50→2.0 exactly→ idx2=200? But expected 140. Doesn't work.

Let me try: idx = p/100 * n: p50: 2.0→200? But expected 140.

OK different methods for different percentiles maybe. p50 uses median (interpolation between middle two). p95/p99 use something else.

Looking again: p95=500. If we take ceiling/nearest-rank: idx=ceil(0.95*4)=4 (1-indexed) = 600. No, that's 600.

Hmm, expected p95=500. What's halfway between 400 and 600? 500. Or 200 and 800? 

Maybe linear interpolation: with x-coords at i/n for i=1..n: positions 0.25, 0.5, 0.75, 1.0 → values 50,80,200,600. p95=0.95: between 0.75(200) and 1.0(600), frac=(0.95-0.75)/0.25=0.8 → 200+0.8*400=520. Not 500.

With positions 0,1/3,2/3,1: p50 at 0.5 → between 1/3,2/3 → frac 0.5 → (80+200)/2=140 ✓. p95 at 0.95 → between 2/3 and 1, frac=(0.95-2/3)/(1/3)=0.85 → 200+0.85*400=540. Not 500.

With positions (i-0.5)/n: 0.125, 0.375, 0.625, 0.875. p50 between 0.375(80),0.625(200): frac=0.5 → 140 ✓. p95: above 0.875, clamp to 600. No.

With positions (i+1)/(n+2)? Strange.

Hmm what if p99 = 580 and p95 = 500 come from a different scheme. 500 - is it median between 200 and... midpoint 4th and 95th? Maybe it's the value at 95% way through sorted+linear from min to max? min=50, max=600. At p95: 50+0.95*550=572.5. No.

Let me try: include 0 implicitly. Latencies [0,50,80,200,600], n=5. positions 0, 0.25, 0.5, 0.75, 1.0. p50→0.5→80? expected 140. No.

What about: latencies treated as cumulative? Sum=930. 50% of 930=465 → cumulative reaches at... 50+80+200=330, +600=930. p50 at 465: into 4th. Probably not.

Let me check p99=580. What gives exactly 580? 80+500. 50*0+80*0.04+200*... hmm. 580 = (580-50)/(600-50) = 530/550 ≈ 0.964. 

Try idx by method R-6: h = (n+1)*p/100. n=4: p50: 2.5 → between idx2,3 (1-indexed) = (80+200)/2=140 ✓. p95: 4.75 → between idx4,5 but only 4 elements → clamp to 600. No.

R-7: h=(n-1)*p/100+1. n=4 p50: 2.5 (1-indexed) → (80+200)/2=140 ✓. p95: 1+0.95*3=3.85 → 200+0.85*400=540. No.

R-8: h=(n+1/3)*p/100+1/3. p50: (4.333)*0.5+0.333=2.5 → 140 ✓. p95: 4.333*0.95+0.333=4.45 → past.

None give 500 and 580.

Let me reverse-engineer. p95=500, p99=580. Difference of 4 in p → diff 80 in value. So slope = 20 per p. At p=95: 500. So p=100 → 600 ✓. p=75 → 100? But 200>100. So linear from some point to max. p=95→500, p=100→600. Backward: p=80→200? Slope is 20/p but 200→500 needs (500-200)/(95-?) Let's see: linear p95=500 p100=600 means value=20p-1400. At what p does value=200? p=80. At p=80 the 3rd element 200, 75% mark. Maybe positions 25, 50, 75, 100 (percentage)? Yes! Position i/n*100 for i=1..n: 25,50,75,100 → 50,80,200,600.

p50: between pos50(80) and pos75(200)? frac=(50-50)/25=0 → 80. But expected 140.

Hmm. Positions 0,33.33,66.67,100? p50 between 33.33 and 66.67: frac=0.5→140 ✓. p95: between 66.67 and 100: frac=(95-66.67)/33.33=0.85→200+0.85*400=540. Not 500.

Positions 12.5, 37.5, 62.5, 87.5? p50: between 37.5(80) and 62.5(200), frac=0.5→140 ✓. p95: past 87.5, clamp to 600. No.

What if p95 interpolates assuming a virtual point at p=100=600 and previous at... different scheme. Already tried.

OK, let me try thinking: p99=580 means actually maybe the formula clamps differently. 580 = 600 - 20. 20 = (100-99)*something. If max stretches from p=95 (value 500) to p=100 (value 600), slope 20/p, then p99=580 ✓ and p95=500. So p95→500 must come from another interpolation between idx2 and idx3 (200 to 600) with frac 0.75. Where does frac 0.75 come from for p95?

If positions are (i-1)/(n-1)*100: 0, 33.33, 66.67, 100. p95: (95-66.67)/33.33=0.85 → 540. No.

What if p95 = mean of last 2 = (200+600)/2 = 400. No, not 500.

p95 = 0.95 * 600 - ... ?  0.95*600=570. No. 

Median of 200, 600, and 600 = 600. Hmm.

Wait, maybe it's `statistics.quantiles` with n=20 (for p95) or just specific values. `statistics.quantiles([50,80,200,600], n=20)` returns 19 cut points using exclusive method. The 19th (idx 18) = 95th percentile. Exclusive: idx = k*(N+1)/n = 19*5/20=4.75. With N=4, clamps... 

Let me actually just compute mentally what statistics.quantiles gives with method='inclusive' n=4 method='inclusive' won't help.

I'll just write code that produces these specific values. Let me see: maybe weighting where p95 and p99 use a different formula. 

What about: