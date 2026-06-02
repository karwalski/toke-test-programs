Let me analyze. Window of 5, values [10.0,10.1,10.0,10.1,10.0], mean=10.04, then need cpk=6.67.

If we use population stdev (pstdev): values [10.0,10.1,10.0,10.1,10.0], mean=10.04, variance = ((0.04)^2*3 + (0.06)^2*2)/5 = (0.0048+0.0072)/5 = 0.0024, stdev=0.04899. cpk_lower=(10.04-9)/(3*0.04899)=1.04/0.1469=7.076. cpk_upper=(11-10.04)/0.1469=6.535. Not 6.67.

Try range/something else. Expected 6.67 = 20/3. Hmm. usl-lsl=2. 

Let me try: maybe it uses the range method. Range = max-min = 0.1. stdev estimate = range/d2 where d2 for n=5 is 2.326. stdev≈0.043. cpk_upper=(11-10.04)/(3*0.043)=0.96/0.129=7.44. No.

What if Cpk = min(usl-mean, mean-lsl)/(3*stdev) with stdev computed differently? 6.67 = (11-10.04)/(3*s) → s=0.048 or (10.04-9)/(3*s)→s=0.052.

Try: min((usl-mean),(mean-lsl))/(3*something). min=0.96. 0.96/(3*s)=6.67 → s=0.048. That matches pstdev ≈0.04899... close but not exact. 0.96/(3*0.048)=6.6667. So s=0.048 exactly.

Hmm, what gives 0.048? Variance 0.002304. Sum of sq deviations = 0.01152. From mean 10.04: deviations 0.04,0.06,0.04,0.06,0.04. Squares: 0.0016*3+0.0036*2=0.0048+0.0072=0.012. /n=0.0024, sqrt=0.04899.

What if mean is rounded? mean=10.04. Hmm.

Try second window [10.1,10.0,10.1,10.0,10.2], mean=10.08, expected cpk=5.0. min(10.08-9,11-10.08)=0.92. 0.92/(3s)=5 → s=0.0613.
pstdev: devs from 10.08: 0.02,0.08,0.02,0.08,0.12. sq: 0.0004+0.0064+0.0004+0.0064+0.0144=0.028. /5=0.0056, sqrt=0.0748. Not 0.0613.

Sample stdev: /4=0.007, sqrt=0.0837. No.

Hmm. Maybe stdev is max-min based? Window 1: range=0.1, s=range/something. 0.96/(3*s)=6.67→s=0.048. 0.1→0.048? ratio 0.48. Window 2: range = 10.2-10.0=0.2. 0.92/(3*s)=5 → s=0.0613. 0.2→0.0613? Ratio 0.307. Not consistent.

Window 3: [10.0,10.1,10.0,10.2,10.3], mean=10.12, expected 3.33. min=0.88. s=0.88/10=0.088. range=0.3.

Maybe it's not using stdev at all. Let me look at the pattern: 6.67, 5.0, 3.33, 2.5, 2.0, 1.67.

6.67≈20/3, 5=15/3, 3.33=10/3, 2.5=7.5/3, 2=6/3, 1.67=5/3.

Or: 6.67=1/0.15, 5=1/0.2, 3.33=1/0.3, 2.5=1/0.4, 2=1/0.5, 1.67=1/0.6.

Hmm denominators 0.15, 0.2, 0.3, 0.4, 0.5, 0.6. Differences in successive windows.

Window 1 last-first index in original: starts move by 1 each time. Maybe (range of window)?
W1 range=0.1, W2=0.2, W3=0.3, W4=0.4, W5=0.5, W6=0.6. Yes!

So Cpk = something / range? 6.67 with range 0.1: 0.667. 5 with 0.2: 1. Not constant.

Or denominator = range * 1.5: W1: 0.15→1/0.15=6.67. ✓ W2: 0.3→3.33. ✗ expected 5.

Hmm. Let me try: 6.67=2/0.3, 5=2/0.4, 3.33=2/0.6, 2.5=2/0.8, 2=2/1.0, 1.67=2/1.2.

Denominators: 0.3, 0.4, 0.6, 0.8, 1.0, 1.2 = 3*range! Where range W1=0.1, W2≈0.133?... 

Actually 0.3/3=0.1=range W1. 0.4/3=0.133. W2 range=0.2. No.

Let me try denominator = 3*(max-min): W1: 3*0.1=0.3, 2/0.3=6.67 ✓. W2: 3*0.2=0.6, 2/0.6=3.33 ✗.

Hmm. Numerator = usl-lsl = 2. W1 6.67=2/0.3. W2 5=2/0.4. W3 3.33=2/0.6. W4 2.5=2/0.8.

So denom: 0.3, 0.4, 0.6, 0.8, 1.0, 1.2. Differences: 0.1, 0.2, 0.2, 0.2, 0.2.

W1 values [10.0,10.1,10.0,10.1,10.0], range 0.1.
W2 [10.1,10.0,10.1,10.0,10.2], range 0.2.
W3 [10.0,10.1,10.0,10.2,10.3], range 0.3.
W4 [10.1,10.0,10.2,10.3,10.4], range 0.4.
W5 [10.0,10.2,10.3,10.4,10.5], range 0.5.
W6 [10.2,10.3,10.4,10.5,10.6], range 0.4.

Denoms: 0.3,0.4,0.6,0.8,1.0,1.2. W6 ratio: 1.2/0.4=3. W5: 1.0/0.5=2. W4: 0.8/0.4=2. W3: 0.6/0.3=2. W2: 0.4/0.2=2. W1: 0.3/0.1=3.

Doesn't fit cleanly. Let me try (usl-lsl)/(6*stdev) — that's Cp not Cpk.

W1 pstdev=0.04899. 2/(6*0.04899)=6.803. Not 6.67.
Sample stdev=0.05477. 2/(6*0.05477)=6.086. No.

Hmm. Let me think differently. Output is Cpk. Standard formula: min((USL-μ)/(3σ), (μ-LSL)/(3σ)).

What if σ is approximated as range/d2 with d2 dependent on window? For n=5, d2=2.326. W1 range 0.1, σ=0.043. min(0.96,1.04)/(3*0.043)=0.96/0.129=7.44. Not matching.

What if σ ≈ range/2 (simple)? W1: σ=0.05. 0.96/0.15=6.4. Close to 6.67 but not exact.

σ = range/something giving exactly 6.67: 0.96/(3σ)=6.67 → σ=0.048. 0.1/0.048=2.083. Not standard.

Hmm. What if it's (USL-LSL)/(6*range)? W1: 2/(6*0.1)=3.33. No.

What if Cpk = min(USL-max, min-LSL)/range or something using min/max? 
W1: min(11-10.1, 10.0-9)=min(0.9,1.0)=0.9. 0.9/0.1=9. No.

(USL+LSL)/2 = 10. min(USL-mean, mean-LSL):
W1 mean 10.04, min=0.96.
W2 mean 10.08, min=0.92.
W3 mean 10.12, min=0.88.
W4 mean 10.2, min=0.8.
W5 mean 10.28, min=0.72.
W6 mean 10.4, min=0.6.

Expected: 6.67, 5, 3.33, 2.5, 2, 1.67.
Ratios = num/expected: 0.96/6.67=0.144, 0.92/5=0.184, 0.88/3.33=0.264, 0.8/2.5=0.32, 0.72/2=0.36, 0.6/1.67=0.36.

0.144,0.184,0.264,0.32,0.36,0.36. /3: 0.048, 0.0613, 0.088, 0.1067, 0.12, 0.12. So implied σ.

W1 σ=0.048, W2 σ=0.0613. Doesn't match pstdev or sstdev.

Hmm, what about mean absolute deviation? 
W1 [10,10.1,10,10.1,10], mean 10.04. MAD = (0.04+0.06+0.04+0.06+0.04)/5 = 0.24/5=0.048. ✓!
W2 [10.1,10.0,10.1,10.0,10.2], mean 10.08. Devs: 0.02,0.08,0.02,0.08,0.12. MAD=0.32/5=0.064. Expected 0.0613. Close but no.

Hmm. Try W2: 0.92/(3*σ)=5 → σ=0.06133. 

What if σ=stdev with a different mean? Like median? W2 median=10.1. Devs from 10.1: 0,0.1,0,0.1,0.1. Squares: 0,0.01,0,0.01,0.01=0.03. /5=0.006, sqrt=0.0775. No. MAD from median=0.3/5=0.06. Closer to 0.0613 but not exact.

What if it uses median absolute deviation? W1: median 10.0, devs 0,0.1,0,0.1,0, MAD=0.04 (mean) or 0 (median of abs)? 

Let me try: maybe σ derived from "moving range" — average of |x[i]-x[i-1]|.
W1 [10,10.1,10,10.1,10]: |0.1|,|0.1|,|0.1|,|0.1|=0.4/4=0.1. σ=MR/1.128=0.0887. No.

Hmm. Let me try yet another: σ as half-range? W2: range=0.2, half=0.1. 0.92/(3*0.1)=3.07. No.

What about Cpk uses the formula differently. Like Cpk = (USL-LSL)/(6σ) — k? where σ is sample range?

Let's look at the relationship between expected values:
6.67, 5, 3.33, 2.5, 2, 1.67. 1/x: 0.15, 0.2, 0.3, 0.4, 0.5, 0.6.

The differences: 0.05, 0.1, 0.1, 0.1, 0.1. Or these = 0.15+0.05*(window#-1) for #=1..6? 0.15, 0.2, 0.25, 0.3, 0.35, 0.4. No, doesn't match (W3 is 0.3 not 0.25).

Or 1/cpk: 0.15, 0.2, 0.3, 0.4, 0.5, 0.6. Ratios 4/3, 3/2, 4/3, 5/4, 6/5.

Hmm look at it: 1/cpk values are 0.15, 0.20, 0.30, 0.40, 0.50, 0.60. These are 3*half_range? Half-ranges: 0.05, 0.1, 0.15, 0.2, 0.25, 0.2. So 3*half range: 0.15, 0.3, 0.45, 0.6, 0.75, 0.6. Doesn't match.

Wait expected cpk 1.67 for W6. 1/1.67=0.6. W6 = [10.2,10.3,10.4,10.