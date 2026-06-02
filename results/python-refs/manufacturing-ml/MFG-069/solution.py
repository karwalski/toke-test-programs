# Let me analyze the expected output to find the actual formula.
# Data: (1,1), (1.1,1.1), (0.9,0.9), (1,1), (5,5)
# Mean: (1.8, 1.8)
# The variables are perfectly correlated, so cov matrix is singular.
# Expected distances: 0.32, 0.95, 0.95, 0.32, 5.37
# 
# Let's see — for point (1,1), diff=(-0.8,-0.8). 
# If we use just variances (diagonal cov): var = sum((x-mean)^2)/(n-1)
# var_s1 = (0.64+0.49+0.81+0.64+10.24)/4 = 12.82/4 = 3.205
# distance from diagonal-only inverse: sqrt(2 * 0.64/3.205) = sqrt(0.3993) = 0.632... not 0.32
#
# Try sqrt of just one dim: sqrt(0.64/3.205) = sqrt(0.1997) = 0.447... no
# 
# Try squared mahalanobis (no sqrt) using diagonal: 2*0.64/3.205 = 0.399... no
#
# Let's check if distances are computed and then divided somehow.
# 0.32 * sqrt(2) ≈ 0.452... 
# Hmm, 0.8/sqrt(3.205) * something. 0.8/sqrt(3.205)=0.447
# 
# What if using population variance (divide by n)? var = 12.82/5 = 2.564
# sqrt(2 * 0.64 / 2.564) = sqrt(0.499) = 0.707... no
#
# 0.32 ≈ 0.8 * 0.4 = 0.32!  0.4 = ? 
# 5.37 for point (5,5): diff=(3.2,3.2). 3.2*1.678=5.37. 
# 0.95 for (1.1,1.1): diff=(-0.7,-0.7). 0.95/0.7 = 1.357
# Ratios differ, so not linear scaling.
#
# Try: distance = |diff_sum|/std where std uses one variable
# (1,1): |-1.6|/std. If std=5, dist=0.32. 5.37: |6.4|/std → std=1.19. inconsistent.
#
# Let me try treating as 1D using sum of vars: s = s1+s2
# values: 2, 2.2, 1.8, 2, 10. mean=3.6. diffs: -1.6,-1.4,-1.8,-1.6,6.4
# variance (n-1): (2.56+1.96+3.24+2.56+40.96)/4 = 51.28/4=12.82, std=3.58
# |diff|/std: 0.447, 0.391, 0.503, 0.447, 1.788... no
#
# Try diff/std with point's own: 
# Actually expected 0.32 and 0.95 — 0.95 ≈ chi-sq threshold-ish? 
# Hmm wait — maybe the threshold for 2 dof 95% is 5.991, sqrt=2.448
# Expected anomaly at idx 4 with dist 5.37 > threshold? threshold could be ~5.99
#
# Let me try: regularized covariance. Add small value to diagonal.
# Actually since perfectly correlated, maybe they used pseudo-inverse or added regularization.
#
# Try cov + epsilon*I where epsilon makes results match.
# For (1,1), diff=(-0.8,-0.8). cov=[[3.205,3.205],[3.205,3.205]].
# With regularization eps: cov'=[[3.205+e,3.205],[3.205,3.205+e]]
# det = (3.205+e)^2 - 3.205^2 = e^2 + 6.41e
# inv = 1/det * [[3.205+e,-3.205],[-3.205,3.205+e]]
# d^T inv d = (1/det)*(0.64*(3.205+e) - 2*0.64*3.205 + 0.64*(3.205+e))
#           = (1/det)*(0.64*2e) = 1.28e/(e^2+6.41e) = 1.28/(e+6.41)
# sqrt = 0.32 → 0.1024 = 1.28/(e+6.41) → e+6.41=12.5 → e=6.09... weird
#
# Hmm. Let me try simpler: maybe just standardize each variable independently (z-score) and use Euclidean.
# var_s1 = 3.205, std=1.7902
# (1,1): z = (-0.8/1.79, -0.8/1.79) = (-0.447,-0.447), euclidean = 0.632... not 0.32
# 
# Half of that = 0.316 ≈ 0.32! So it's z-score average or sqrt(z^2)/sqrt(2)?
# 0.632/2 = 0.316. For (5,5): z=(3.2/1.79)=1.788, euclidean=2.528, /2=1.264. Not 5.37.
#
# Not that either. Let me think about 5.37 for diff (3.2, 3.2).
# 5.37/3.2 = 1.678. And 0.32/0.8 = 0.4. Different scaling.
# 0.95/0.7 = 1.357. 0.95/0.9=1.056 (for diff 0.9 from (0.9,0.9)→diff=-0.9).
# Wait (0.9,0.9) diff = (-0.9,-0.9). 0.95/0.9 = 1.056.
# (1.1,1.1) diff=(-0.7,-0.7). 0.95/0.7=1.357.
# But both give 0.95! So it's not |diff|*const.
#
# Maybe Mahalanobis squared? 0.32, 0.95, 0.95, 0.32, 5.37 sum = 7.91
# For chi-sq with df=2, expected sum E[d^2]=df*(n-1)... hmm sum=2*(5-1)/5*... 
# Actually sum of squared Mahalanobis = (n-1)*p = 4*2 = 8. Close to 7.91!
# So these ARE squared Mahalanobis distances (not square-rooted).
#
# Let me recompute without sqrt, using pseudo-inverse or proper handling.
# Since cov is singular (perfect correlation), need pseudoinverse.
# Eigendecomp of [[3.205,3.205],[3.205,3.205]]: eigenvalues 6.41 and 0, eigenvectors (1,1)/sqrt2 and (1,-1)/sqrt2.
# Pseudoinverse: (1/6.41) * (1,1)(1,1)^T/2 = [[1/12.82, 1/12.82],[1/12.82,1/12.82]]
# For (1,1) diff=(-0.8,-0.8): d^T M d = 4*0.64/12.82 = 2.56/12.82 = 0.1997... not 0.32
#
# Hmm 0.1997 ≈ 0.20, but expected 0.32. Ratio 0.32/0.1997 = 1.6 = 8/5 = n/(n-1)?
# Try population covariance (divide by n=5): var=12.82/5=2.564
# Pseudoinv eigenvalue: 1/(2*2.564) = 0.195
# d^T M d for (-0.8,-0.8): 4*0.64*0.195=0.4992... no
#
# Let me try: pseudoinverse using sample cov with n-1, and the formula gives 0.1997 for (1,1).
# Hmm 0.32 vs 0.1997. What if it's sum/(n-p)? 
# Actually, let me recompute. For (5,5), diff=(3.2,3.2). 
# d^T M d = 4*3.2^2/12.82 = 40.96/12.82 = 3.195. But expected 5.37!
# So not that.
#
# Let me try with population variance n=5: var_sum = 51.28/5 = 10.256
# pseudoinv element = 1/(2*10.256) = 0.04876
# (5,5): 4*10.24*0.04876 = 1.997. No.
#
# Try: 1D analysis on sum or single variable. s1 values: 1,1.1,0.9,1,5. mean=1.8. 
# var (n-1) = ((0.8)^2+(0.7)^2+(0.9)^2+(0.8)^2+(3.2)^2)/4 = (0.64+0.49+0.81+0.64+10.24)/4 = 12.82/4 = 3.205
# Squared mahalanobis 1D = diff^2/var:
# 0.64/3.205=0.1997, 0.49/3.205=0.153, 0.81/3.205=0.253, 0.1997, 10.24/3.205=3.195
# Expected: 0.32, 0.95, 0.95, 0.32, 5.37. Ratios: 1.6, 6.2, 3.75, 1.6, 1.68. Not constant.
#
# What if cov computed differently? Let me check if expected output uses some specific library convention.
# 
# Try: scipy-like with bias=True (divide by n). var = 12.82/5 = 2.564. 
# 1D: 0.64/2.564=0.2496, 0.49/2.564=0.191, 0.81/2.564=0.316, 0.2496, 10.24/2.564=3.994
# Hmm 0.316 ≈ 0.32 for point 3! And 0.2496 ≈ 0.25 (expected 0.32 for point 1).
# Not matching.
#
# What if the values 0.32, 0.95, 0.95, 0.32, 5.37 use distance not squared?
# sqrt: 0.566, 0.975, 0.975, 0.566, 2.317. Hmm, two 0.975's.
# Sum of squares: 0.32+0.95+0.95+0.32+5.37 = 7.91. Sum of distances squared in actual mahalanobis = trace = (n-1)*p for sample.
# Actually for sample Mahalanobis with sample cov, sum_i (x_i-μ)^T S^-1 (x_i-μ) = (n-1)*p
# Here = 4*2 = 8. We got 7.91. Close but using pseudoinverse with df=1 (since rank 1), sum = (n-1)*rank = 4.
# 7.91 doesn't match either cleanly. Hmm.
#
# Let me check 0.95 and 0.95 — points (1.1,1.1) and (0.9,0.9). Their diffs from mean (1.8,1.8) are (-0.7,-0.7) and (-0.9,-0.9). They have DIFFERENT magnitudes but same Mahalanobis distance? That's impossible if cov is fixed and diff direction is the same...
# UNLESS it's leave-one-out!
#
# Yes! Leave-one-out Mahalanobis. Recompute mean and cov excluding the point itself.
# Let me verify for point 1 (1.0, 1.0):
# Other points: (1.1,1.1),(0.9,0.9),(1.0,1.0),(5.0,5.0). mean=(2.0,2.0). 
# diffs from new mean: each var diff: -0.9, -1.1, -1.0, 3.0. var = (0.81+1.21+1+9)/3 = 12.02/3 = 4.0067
# For excluded point (1,1): diff = (-1, -1). 
# Cov still singular. 1D squared: 1/4.0067 = 0.2496. Hmm not 0.32.
#
# Try point 2 (1.1, 1.1): others mean = (1+0.9+1+5)/4 = 7.9/4 = 1.975
# diffs: -0.975, -1.075, -0.975, 3.025. var = (0.9506+1.1556+0.9506+9.1506)/3 = 12.2075/3 = 4.0692
# diff for (1.1,1.1) from mean 1.975: -0.875. squared/var = 0.7656/4.0692 = 0.188. Not 0.95.
#
# Not leave-