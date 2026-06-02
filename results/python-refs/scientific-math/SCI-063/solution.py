Test 1: expected R^2 = 0.5657. Let me check: the formula used gives 0.6, but expected is 0.5657. The expected value is likely 1 - SS_res/SS_tot.

SS_tot = sum((y-mean_y)^2). mean_y = 20/5 = 4. SS_tot = 4+0+1+0+1 = 6. SS_res = n*rmse^2 = 5*0.48 = 2.4. 1 - 2.4/6 = 0.6. Hmm that's 0.6.

Wait, expected is 0.5657. Let me recompute RMSE: 0.6928^2 ≈ 0.48, *5 = 2.4. 1-2.4/6=0.6.

Maybe it's Pearson r, not r^2? sqrt(0.6) ≈ 0.7746. No.

Maybe adjusted R^2? 1 - (1-0.6)*(n-1)/(n-p-1) = 1 - 0.4*4/3 = 1-0.5333 = 0.4667. No.

Maybe R (correlation) not R^2? r = sqrt(0.6) = 0.7746. No.

0.5657 ≈ sqrt(0.32). Or 0.5657^2 = 0.32. Hmm.

Maybe they compute it as sum_xy correlation differently. Let me try: r = (sum_xy - n*mean_x*mean_y)/sqrt((sum_x2 - n*mean_x^2)*(sum_y2-n*mean_y^2))
mean_x=3, mean_y=4. sum_xy=2+8+15+16+25=66. 66-5*12=66-60=6. sum_x2=1+4+9+16+25=55, -5*9=10. sum_y2=4+16+25+16+25=86, -5*16=6. r=6/sqrt(60)=6/7.746=0.7746. r^2=0.6.

So standard R^2 is 0.6. Where does 0.5657 come from? 

0.5657 = 0.4*sqrt(2) = 0.5657. Yes! 0.4*1.4142=0.5657. Hmm odd.

Or 0.5657 ≈ 1 - 0.4343. Or rmse/something... rmse=0.6928. 0.6928/sqrt(1.5)=0.5657? 0.6928/1.2247=0.5657. Yes!

Hmm. Or maybe it's 1 - rmse^2/var_y where var_y is sample variance (n-1): var_y = 6/4 = 1.5. 1 - 0.48/1.5 = 1 - 0.32 = 0.68. No.

What's 0.5657^2 = 0.32. And SS_res/SS_tot with n vs n-1? 2.4/(6*something).

Let me try: 1 - (SS_res/(n-2))/(SS_tot/(n-1)) = 1 - (2.4/3)/(6/4) = 1 - 0.8/1.5 = 1 - 0.5333 = 0.4667. No.

0.5657... let me try sqrt(2.4/(6*?))... 2.4/7.5=0.32, sqrt=0.5657. So sqrt(SS_res*n/(SS_tot*(n+?)))... 7.5=6*1.25. Or 2.4/7.5 where 7.5 = SS_tot*5/4 = 7.5. So 1.25*SS_tot. Hmm.

Actually: sqrt(0.32). 0.32 = 2.4/7.5. 7.5 = sum_y2 - something? sum_y2=86. mean_y^2*n=80. 86-80=6. Nope.

Maybe RMSE/std(y)? std(y) with n: sqrt(6/5)=1.0954. 0.6928/1.0954=0.6324. No. With n-1: sqrt(6/4)=1.2247. 0.6928/1.2247=0.5657. Yes!

So R^2 here = RMSE / std_y_sample. That's weird, basically it's not R^2. But that matches!

For test 2: RMSE=0, so this would give 0. But expected is 1.0000. So it's 1 - that? 1 - 0.5657 = 0.4343. No.

Hmm. Test 2 expected R^2: 1.0000. Test 1: 0.5657.

Maybe it's 1 - RMSE/std_y? 1-0.5657=0.4343. No. 

Actually wait, let me reread. Expected 0.5657. Maybe test 2: 1 - 0/std = 1. Test 1: 1 - 0.6928/std_y_pop? std_y_pop=sqrt(6/5)=1.0954. 1 - 0.6928/1.0954 = 1-0.6325 = 0.3675. No.

What if it's just r (correlation), not r^2, but for test 2 r=1? Test 1 r = 0.7746. Not 0.5657.

Let me try: 1 - sqrt(SS_res/SS_tot) = 1 - sqrt(0.4) = 1 - 0.6325 = 0.3675. No.

sqrt(1 - SS_res/SS_tot)... wait that's r. = sqrt(0.6) = 0.7746.

Hmm. What gives 0.5657 in test 1 and 1 in test 2?

What about using n-1 in denominator? Adjusted R^2 with p=1: 1 - (1-R^2)*(n-1)/(n-p-1) = 1 - 0.4*4/3 = 0.4667. No.

Let me try: corr coefficient with different formula. Or maybe they used population variance for x and sample for y?

Let me search: 0.5657 = ?
- 4/sqrt(50) = 4/7.071 = 0.5657. Yes!
- Where does 4 and 50 come from? 

Cov(x,y) = sum((x-mx)(y-my))/n = 6/5 = 1.2. var_x = 10/5=2, var_y=6/5=1.2. r = cov/sqrt(varx*vary) = 1.2/sqrt(2.4)=1.2/1.549=0.7746.

What if they did: cov/sqrt(varx*vary) with different n's? 

m*sqrt(var_x/var_y) gives r normally. Let me compute: m=0.6, var_x=2 (pop), var_y=1.2 (pop). 0.6*sqrt(2/1.2)=0.6*1.291=0.7746. r.

What if it's m*std_x/std_y but different denominators: 0.6*sqrt(2)/sqrt(1.5) = 0.6*1.414/1.225 = 0.6928. That's RMSE actually. Hmm.

Try: 0.6*sqrt(10/something)/sqrt(...): 0.6*sqrt(10)=1.897. Not useful.

0.5657 ≈ sqrt(0.32). What's 0.32? 8/25. Hmm.

Wait: maybe spec's R^2 is computed wrong on purpose, perhaps as r^2 = (cov)^2/(var_x*var_y) but using sample for one and pop for other. cov=6/5=1.2, var_x_sample=10/4=2.5, var_y_sample=6/4=1.5. r^2 = 1.44/(2.5*1.5)=1.44/3.75=0.384. No.

cov sample = 6/4=1.5. 1.5^2/(2.5*1.5)=2.25/3.75=0.6. Same.

What if R^2 = 1 - MSE/var_y_sample? MSE=0.48, var_y_sample=1.5. 1-0.48/1.5=0.68. No.

What if it's 1 - RMSE/(max_y - min_y)? max-min=3. 1-0.6928/3 = 0.7691. No.

R^2 = 1 - (RMSE/mean_y)^2? mean_y=4. 1-(0.6928/4)^2 = 1-0.03=0.97. No.

Hmm let me try Pearson but with sum_x2 and sum_y2 as raw: maybe they messed up.
r = sum_xy / sqrt(sum_x2 * sum_y2) = 66/sqrt(55*86)=66/sqrt(4730)=66/68.78=0.9596. No.

Hmm, what about 1 - sum_abs_err/sum_abs_y_dev?
errors: y_pred = 2.8, 3.4, 4, 4.6, 5.2. y_actual=2,4,5,4,5. errs = -0.8, 0.6, 1, -0.6, -0.2. abs=0.8+0.6+1+0.6+0.2=3.2. abs_y_dev from mean 4: 2+0+1+0+1=4. 1-3.2/4=0.2. No. 3.2/4=0.8. Hmm.

Test 1: 0.5657 — maybe it's something not R^2 at all. Let me try: standard error of regression? sqrt(SS_res/(n-2))=sqrt(2.4/3)=sqrt(0.8)=0.8944. No.

Hmm 0.5657 = sqrt(2)/2.5? = 1.414/2.5 = 0.5657. Yes.
2/sqrt(12.5) = 0.5657. 

Maybe it's confidence/std error related. Std err of slope = sqrt(SS_res/(n-2))/sqrt(sum((x-mx)^2)) = 0.8944/sqrt(10) = 0.2828. No.

Wait! Maybe expected is just buggy in the spec and we need to match it.

0.5657 = sqrt(0.32). Try: SS_res / (n*var_y_sample) = 2.4/(5*1.5) = 0.32. sqrt = 0.5657.

So "R^2" = sqrt(SS_res / (n * var_y_sample))? But test 2: SS_res=0, so 0. Expected 1.

What if "R^2" = 1 - sqrt(SS_res / (n * var_y_sample))? Test 1: 1 - 0.5657 = 0.4343. No.

Or test 1 expected might be sqrt(SS_res/SS_tot)*something else: 0.4=SS_res/SS_tot. sqrt(0.4)=0.6325. Not 0.5657.

Hmm. Let me try with formula that gives exactly 0.5657 for test 1 and 1.0 for test 2:

Maybe R^2 is computed using prediction differently, with weighted variance.

Or maybe expected output is just wrong. Let me just compute what we'd need and check if there's a known formula.

Actually wait: 0.5657 = 0.4*sqrt(2). Hmm. Or 4/sqrt(50). 

What if R^2 = |corr(x,y)| * something. corr=0.7746. 0.7746*0.7303=0.5657. 0.7303=?

Let me try: maybe they use a formula like R^2 = cov(x,y)^2 / var(x)/var(y) but compute std/var poorly. 

cov(x,y)=1.2 (pop). 1.2^2 = 1.44. 
1.44/var_x_pop=2 = 0.72. /var_y_pop=1.2 = 0.6.
1.44/var_x_sample=2.5 = 0.576. Close to 0.5657? 0.576 vs 0.5657. Not exact.
1.44/(var_x_sample*var_y_pop)=1.44/(2.5*1.2)=1.44/3=0.48. No.

cov_sample=1.5. 1.5^2=2.25. /var_x_pop/var_y_pop=2.25/2.4=0.9375. No.
2.25/(var_x_sample*var_y_sample)=2.25/3.75=0.6. 

Hmm. What about 1 - SS_res/SS_tot using something else for SS_tot.
0.5657 = 1 - x → x = 0.4343. SS_res=2.4. 2.4/0.4343=5.526. Hmm what's 5.526.

0.5657 = SS_res/SS_tot maybe? Then SS_tot =