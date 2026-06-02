Let me analyze the expected output. With data:
- (10,20), (10.1,20.1), (9.9,19.9), (10,20), (12,22)
- mean = (10.4, 20.4)

Expected t_squared: [0.0, 0.5, 0.5, 0.0, 20.0]

For point 5: diff = (1.6, 1.6). Let me check covariance with diagonal only or something...

Actually, let me compute: var(x1) = ((0.4)² + (0.3)² + (0.5)² + (0.4)² + (1.6)²)/4 = (0.16+0.09+0.25+0.16+2.56)/4 = 3.22/4 = 0.805

Hmm. Maybe they use n instead of n-1: 3.22/5 = 0.644

For point 1: diff=(-0.4,-0.4). T² = 0.0? That means the formula gives 0 when diffs are equal? That happens if cov is singular (perfectly correlated).

Looking at data: x2 = x1 + 10 exactly for all points! So they're perfectly correlated, cov is singular.

Expected: point with diff (1.6,1.6) gives 20.0. With diff (-0.4,-0.4) gives 0?? That's weird.

Wait, maybe it's using only the diagonal (variance per variable, ignoring covariance):
T² = sum(diff_i² / var_i)

var(x1) with n-1=4: 3.22/4 = 0.805
Point 1: 0.16/0.805 + 0.16/0.805 = 0.397... not 0.

Let me try: maybe compute T² differently per row using the formula with mean subtraction but treat... 

Expected [0, 0.5, 0.5, 0, 20]. Sum = 21. With p=2, n=5, sum of T² should be p(n-1) = 8 for standard. Doesn't match.

Maybe t_squared uses range or different scaling. Let me try: diff² total:
Row1: 0.16+0.16=0.32
Row2: 0.09+0.09=0.18
Row3: 0.25+0.25=0.50
Row4: 0.16+0.16=0.32
Row5: 2.56+2.56=5.12

Hmm row 3 gives 0.50 which matches! Row 5: 5.12 ≠ 20.

What if subtract from first point (not mean)?
Row1: (0,0) → 0 ✓
Row2: (0.1,0.1) → 0.02 ✗

What about diff from median? median = (10, 20).
Row1: (0,0) → 0 ✓
Row2: (0.1,0.1) → sum sq = 0.02
Row3: (-0.1,-0.1) → 0.02
Row4: (0,0) → 0 ✓
Row5: (2,2) → 8

Hmm row 5 = 8, not 20. But ratio 20/8 = 2.5.

What if T² = (x-median)ᵀ S⁻¹ (x-median) but with diagonal cov only?
var with median, n-1: ((0)+(0.01)+(0.01)+0+4)/4 = 4.02/4 = 1.005
Row5: 4/1.005 + 4/1.005 ≈ 7.96. No.

What if using sample range as scale?

Try sum sq diff from median with var using n:
var = 4.02/5 = 0.804
Row5: 4/0.804 * 2 ≈ 9.95. No.

Let me think differently. Expected row5=20, row3=0.5. Ratio 40.

What if T² = n*(diff·diff)/something? Row1=0, Row5=20. For row5 diff from mean: (1.6,1.6). 

Actually maybe they pseudo-invert with only diagonal of cov:
cov diagonal: var = 3.22/4 = 0.805
Row5: (1.6²+1.6²)/0.805 = 5.12/0.805 = 6.36. Not 20.

With n=5 divisor: 3.22/5 = 0.644, 5.12/0.644 = 7.95. No.

What if variance is calculated differently — maybe just x1 variance from differences row-to-row?

Let me check: maybe T² computed via per-component (x_i - mean)² / variance where each component standardized:
For row 5: ((1.6)/std)² + ((1.6)/std)²
If std² = ?  to give 20: 2*2.56/s² = 20 → s² = 0.256, s=0.506.

What variance gives 0.256? Sum sq devs = 0.256*k. If k=5: total=1.28. Our sum sq devs=3.22. If k=12.578... no.

What if using only 4 in-control points (excluding outlier)?
mean of first 4: (10, 20). var(x1) = (0+0.01+0.01+0)/3 = 0.00667
Row5: diff = (2,2). (4+4)/0.00667 = 1200. No.

With n=4: 0.02/4 = 0.005, 8/0.005 = 1600. No.

Hmm, let me try: diff from first-4 mean, divide by var of first 4:
Var first 4 (n-1=3): 0.02/3 = 0.00667 each
Row1: (0,0) → 0 ✓
Row2: (0.1,0.1) → 0.01/0.00667 *2 = 3
Row3: (-0.1,-0.1) → 3
Row4: 0 ✓  
Row5: (2,2) → 4/0.00667 *2 = 1200

Not matching.

What if diff² / variance using sample variance over all 5 with n divisor:
var = 3.22/5 = 0.644
Row1: 0.32/0.644 = 0.497 ≈ 0.5? But expected 0.
Row3: 0.5/0.644 = 0.776

Hmm.

Let me try: maybe Hotelling with the singular cov handled by adding diagonal:
Actually wait, maybe expected divides by sum or has off-by-one.

For row 5 to be 20 and row 3 to be 0.5, ratio = 40 = (1.6/0.5)² *... = 10.24. With ratio of diff²: 5.12/0.5 = 10.24. So actual ratio of T²=40 vs diff² ratio=10.24. Means scaling isn't just constant.

Unless distance metric isn't quadratic in diff. Maybe Mahalanobis squared = ((x-μ)ᵀ(x-μ))² /something? Row3: 0.25, Row5: 26.21. Ratio 105. No.

Or: T² = (x-μ)ᵀ(x-μ)·n/p maybe related to mean.

Let me check sum of T²: 0+0.5+0.5+0+20 = 21. Hmm.

Sum (x-mean)² over both cols: 0.32+0.18+0.5+0.32+5.12 = 6.44 = sum of squared distances from centroid.

For row 5 alone: 5.12. T²=20. Ratio = 3.906. 
For row 3: 0.5, T²=0.5. Ratio = 1.
For row 2: 0.18, T²=0.5. Ratio = 2.78.
For row 1: 0.32, T²=0. Ratio undefined.

This is confusing. Maybe the spec computation rounds to certain values, or maybe uses individual variances:

var(x1) using n: 0.644. T²_x1 component: diff²/var
Row1: 0.16/0.644 = 0.248 → not 0

Let me think: what if it computes (x_i - x_bar)² / σ² with σ² = MSE from regression or something? Given x2=x1+10, the data has perfect correlation.

Maybe expected uses a specific simplification: T² = diff_x1² + diff_x2² as raw, then for row5 the variance somehow becomes 0.256... 

Actually, given the variance ratio for variance to give T²=20 at diff=(1.6,1.6): we need 2*2.56/s² = 20, s² = 0.256.

For T²=0.5 at row 3 with diff=(-0.5,-0.5): 2*0.25/s² = 0.5, s² = 1.0.

For row 2 with diff=(-0.3,-0.3): 2*0.09/s² = 0.5, s² = 0.36.

These s² values differ, so it's not constant. Each row has its own?

What's special: row 2 s²=0.36 = 0.6², row 3 s²=1.0, row 5 s²=0.256.

Hmm. 

What if it's actually using neighboring differences (successive differences method)?
Differences between consecutive: (0.1,0.1), (-0.2,-0.2), (0.1,0.1), (2,2)
Sum sq / 2(n-1): variance estimator

V = sum of (diff_consecutive)²/2 / (n-1) for each variable
= (0.01+0.04+0.01+4)/2/4 = 4.06/8 = 0.5075

Row 5: (1.6²+1.6²)/0.5075 = 5.12/0.5075 = 10.09. Not 20.

What if it's just hardcoded expected output that someone chose to make a "nice" test? Let me check if there's a simple formula.

Actually let me look at expected more carefully:
[0.0, 0.5, 0.5, 0.0, 20.0]

Maybe it's diff_from_median² summed × some factor?
median (per col) = 10, 20
diffs from median: (0,0), (0.1,0.1), (-0.1,-0.1), (0,0), (2,2)
sum sq: 0, 0.02, 0.02, 0, 8

Not matching 0,0.5,0.5,0,20.

But ratio: 0.5/0.02 = 25, 20/8 = 2.5. Not consistent.

Hmm, what about: sum_sq * (something based on n)?

Wait, let me see if maybe x1 only:
diff_x1²: 0.16, 0.09, 0.25, 0.16, 2.56. With var(x1):
var n-1: 0.805. Vals: 0.199, 0.112, 0.310, 0.199, 3.18

With var n=4 (n-1 using only 4 first): 0.00667. Vals: 24, 13.5, 37.5, 24, 384.

With var calculated differently...

Maybe MR (moving range)?
|x1 diffs|: 0.1, 0.2, 0.1, 2.0
mean MR = 0.6
σ̂ = MR_bar / d2 (d2=1.128) = 0.532
σ̂² = 0.283
Row5: 2.56/0.283 = 9.04, *2 = 18.08. Close to 20 but not exact.

With σ̂² = 0.256 exactly:
Row5: 5.12/0.256 = 20 ✓
Row3: 0.5/0.256 = 1.95 ✗

So no.

Maybe per-row variance is just diff² of that row?

What if T² = (sum diff²) × n / sum(all diff²)?
Row5: 5.12 * 5 / 6.44 = 3.97. No.

OK at this point, let me try yet another approach. What if the expected uses pooled variance from first 4 (in-control) rows then applies to all:

First 4 mean: (10, 20)
var per col (n-1=3): 0.02/3 = 0.00667
But x2 = x1+10 exactly in first 4, cov singular.

Use diagonal only: T² = diff_x1²/var + diff_x2²/var
Row1 from mean (10,20): (0,0) → 0 ✓
Row2: (0.1,0.1): 0.01/0.00667 * 2 = 3.0 ✗

Doesn't match expected 0.5.

What if variance is computed across ALL data including outlier, but mean is from first 4?
mean=(10,20), var (n-1=4 all data, x1): ((10-10)²+(10.1-10)²+(9.9-10)²+(10-10)²+(12-10)²)/4 = (0+0.01+0.01+0+4)/4 = 1.005

Row1: 0/1.005 + 0/1.005 = 0 ✓