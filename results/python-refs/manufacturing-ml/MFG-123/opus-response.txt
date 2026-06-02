I need to figure out what coefficients are expected. Expected: A=76, B=95, C=60.

Let me check: data points are (0.5,0.3,0.2,80), (0.4,0.4,0.2,85), (0.3,0.3,0.4,75), (0.6,0.2,0.2,78).

With coefficients A=76, B=95, C=60:
- 0.5*76 + 0.3*95 + 0.2*60 = 38 + 28.5 + 12 = 78.5 (actual 80)
- 0.4*76 + 0.4*95 + 0.2*60 = 30.4 + 38 + 12 = 80.4 (actual 85)
- 0.3*76 + 0.3*95 + 0.4*60 = 22.8 + 28.5 + 24 = 75.3 (actual 75)
- 0.6*76 + 0.2*95 + 0.2*60 = 45.6 + 19 + 12 = 76.6 (actual 78)

Not exact fit. Hmm. My computed (76.5, 111.5, 46.5) should be least-squares optimal. Let me verify:
- 0.5*76.5 + 0.3*111.5 + 0.2*46.5 = 38.25 + 33.45 + 9.3 = 81.0
- 0.4*76.5 + 0.4*111.5 + 0.2*46.5 = 30.6 + 44.6 + 9.3 = 84.5
- 0.3*76.5 + 0.3*111.5 + 0.4*46.5 = 22.95 + 33.45 + 18.6 = 75.0
- 0.6*76.5 + 0.2*111.5 + 0.2*46.5 = 45.9 + 22.3 + 9.3 = 77.5

Residuals: (-1, 0.5, 0, 0.5). Sum of squares = 1.5.

Expected residuals: (1.5, 4.6, -0.3, 1.4). SSE = 2.25+21.16+0.09+1.96=25.46. Much worse fit.

So expected isn't OLS. Maybe it's solving with first 3 equations directly?
- 0.5A + 0.3B + 0.2C = 80
- 0.4A + 0.4B + 0.2C = 85
- 0.3A + 0.3B + 0.4C = 75

From eq2-eq1: -0.1A + 0.1B = 5 → B-A = 50, B = A+50
From eq1: 0.5A + 0.3(A+50) + 0.2C = 80 → 0.8A + 15 + 0.2C = 80 → 0.8A + 0.2C = 65 → 4A+C=325
From eq3: 0.3A + 0.3(A+50) + 0.4C = 75 → 0.6A + 15 + 0.4C = 75 → 0.6A + 0.4C = 60 → 3A+2C=300

From 4A+C=325: C=325-4A. Sub: 3A + 2(325-4A) = 300 → 3A+650-8A=300 → -5A=-350 → A=70, C=45, B=120.

Not matching. Let me try average-based approach. Mean A=0.45, B=0.3, C=0.25, mean y=79.5.

Maybe expected is solving last 3 equations?
- 0.4A+0.4B+0.2C=85
- 0.3A+0.3B+0.4C=75
- 0.6A+0.2B+0.2C=78

eq1-eq3: -0.2A+0.2B = 7 → B-A=35, B=A+35
eq1: 0.4A+0.4(A+35)+0.2C=85 → 0.8A+14+0.2C=85 → 0.8A+0.2C=71 → 4A+C=355
eq2: 0.3A+0.3(A+35)+0.4C=75 → 0.6A+10.5+0.4C=75 → 0.6A+0.4C=64.5 → 3A+2C=322.5
C=355-4A: 3A+710-8A=322.5 → -5A=-387.5 → A=77.5, C=45, B=112.5. No.

Let me try: maybe they used pseudo-inverse differently or rounded coefficients. A=76, B=95, C=60. Notice B-A=19, A-C=16. 

Maybe simple average per-component-weighted? sum(x_i*y)/sum(x_i):
- A: (0.5*80+0.4*85+0.3*75+0.6*78)/(0.5+0.4+0.3+0.6) = (40+34+22.5+46.8)/1.8 = 143.3/1.8 = 79.61
No.

Maybe expected coefficients come from a different formula. Let me try: coefficient_i = y when x_i=1. Extrapolation via specific method.

Actually let me check if expected is consistent with some scheme: A=76, B=95, C=60, mean=77. Check if 0.45*76+0.3*95+0.25*60 = 34.2+28.5+15 = 77.7. Mean y = 79.5. Doesn't match either.

Let me try regression with intercept where intercept=0 enforced differently. Or maybe Scheffe with cross terms but reported only linear part.

Let me try centered: subtract mean of each x. xc_A = x_A - 0.45, etc. But components sum to 1, so centered sum to 0.

Let me try: solve only 3 equations using rows 1, 2, 4:
- 0.5A+0.3B+0.2C=80
- 0.4A+0.4B+0.2C=85  
- 0.6A+0.2B+0.2C=78

eq1-eq2: 0.1A-0.1B=-5 → A-B=-50, B=A+50
eq1-eq3: -0.1A+0.1B=2 → B-A=20. Contradiction. So this trio inconsistent.

Hmm. Let me search: maybe gradient descent with limited iterations? Or specific intercept... 

Let me check: average of pairs? Or coefficient = response when that component dominates?
- Highest A=0.6, y=78. 
- Highest B=0.4 (row 2), y=85.
- Highest C=0.4, y=75.

What if extrapolation? For A: at A=0.6, y=78. Slope of A... 

Let me try: model y = bA*A + bB*B + bC*C, fit using least squares but with different weight or normalization.

Actually let me just try if (76, 95, 60) satisfies any specific 3 equations via some weighted approach. 

Pseudo-inverse: β = (X^T X)^-1 X^T y. I got (76.5, 111.5, 46.5). 

What if they used X^T y / diagonal of X^T X?
X^T y: 
- A: 0.5*80+0.4*85+0.3*75+0.6*78 = 40+34+22.5+46.8 = 143.3
- B: 0.3*80+0.4*85+0.3*75+0.2*78 = 24+34+22.5+15.6 = 96.1
- C: 0.2*80+0.2*85+0.4*75+0.2*78 = 16+17+30+15.6 = 78.6

Diag of X^T X:
- A: 0.25+0.16+0.09+0.36 = 0.86
- B: 0.09+0.16+0.09+0.04 = 0.38
- C: 0.04+0.04+0.16+0.04 = 0.28

143.3/0.86 = 166.6, no.

Let me try simpler: weighted mean. y_pred at pure i. Maybe coefficient_i = sum(y_k * x_ki) / sum(x_ki)... already tried.

Let me look: 76, 95, 60. Differences 95-76=19, 76-60=16. Sum=231, avg=77.

What if regression using just normal equations but with a "centered" approach — adding a virtual datapoint?

Let me try: solve full 4 equations in least squares but with a particular regularization or constraint.

Actually let me check if these are from an "intercept" model converted: if y = b0 + b1*A + b2*B (with C as reference), maybe. Set C=1-A-B then y = b0 + (b1-bC)*A + (b2-bC)*B + bC. So intercept = bC = 60, and bA = b0' + 60 = 76 → b0'=16, bB = b0'+60 = 95 → b0' for B = 35. So fit y = 60 + 16*A + 35*B as linear in A and B with intercept 60.

Let me OLS-fit y = β0 + β1*A + β2*B (3 params, 4 data points):
Data: (A, B, y) = (0.5, 0.3, 80), (0.4, 0.4, 85), (0.3, 0.3, 75), (0.6, 0.2, 78)

Sums: n=4, ΣA=1.8, ΣB=1.2, Σy=318, ΣA²=0.86, ΣB²=0.38, ΣAB=0.5*0.3+0.4*0.4+0.3*0.3+0.6*0.2=0.15+0.16+0.09+0.12=0.52
ΣAy=143.3, ΣBy=96.1

Normal equations:
4β0 + 1.8β1 + 1.2β2 = 318
1.8β0 + 0.86β1 + 0.52β2 = 143.3
1.2β0 + 0.52β1 + 0.38β2 = 96.1

Let me solve. From eq1: β0 = (318 - 1.8β1 - 1.2β2)/4 = 79.5 - 0.45β1 - 0.3β2

Sub eq2: 1.8(79.5 - 0.45β1 - 0.3β2) + 0.86β1 + 0.52β2 = 143.3
143.1 - 0.81β1 - 0.54β2 + 0.86β1 + 0.52β2 = 143.3
0.05β1 - 0.02β2 = 0.2 → 5β1 - 2β2 = 20

Sub eq3: 1.2(79.5 - 0.45β1 - 0.3β2) + 0.52β1 + 0.38β2 = 96.1
95.4 - 0.54β1 - 0.36β2 + 0.52β1 + 0.38β2 = 96.1
-0.02β1 + 0.02β2 = 0.7 → -β1 + β2 = 35 → β2 = β1 + 35

Sub: 5β1 - 2(β1+35) = 20 → 3β1 = 90 → β1 = 30, β2 = 65? 

Hmm not 16 and 35. Let me recheck. Actually β0 = 79.5 - 0.45*30 - 0.3*65 = 79.5 - 13.5 - 19.5 = 46.5.

So fit: y = 46.5 + 30A + 65B, and bC = 46.5, bA = 46.5+30 = 76.5, bB = 46.5+65 = 111.5. That matches my OLS answer! (Of course, equivalent reparam.)

So expected (76, 95, 60) is NOT OLS. Let me check what produces this.

Maybe they fit using only 3 data points (dropping one)?

Let me try dropping each row and OLS-fitting the remaining 3 exactly:

Drop row 1: solve exactly rows 2,3,4:
- 0.4A+0.4B+0.2C=85
- 0.3A+0.3B+0.4C=75
- 0.6A+0.2B+0.2C=78
(I computed earlier: A=77.5, B=112.5, C=45)

Drop row 2: rows 1,3,4:
- 0.5A+0.3B+0.2C=80
- 0.3A+0.3B+0.4C=75
- 0.6A+0.2B+0.2C=78
eq1-eq3: -0.1A+0.1B=2 → B=A+20
eq1: 0.5A+0.3(A+20)+0.2C=80 → 0.8A+6+0.2C=80 → 4A+C=370
eq2: 0.3A+0.3(A+20)+0.4C=75 → 0.6A+6+0.4C=75 → 3A+2C=345
C=370-4