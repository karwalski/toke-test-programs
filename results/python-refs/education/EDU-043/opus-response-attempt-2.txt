Looking at the data:
- Raw: 80,70,60,90,50, mean=70, var(pop)=200
- Expected: 79.0, 72.1, 65.2, 85.9, 58.3
- These fit: adjusted = 0.69*raw + 23.8, with k=0.690 = 10/sqrt(210), shift derivation needs checking.

Let me verify: k=10/sqrt(210)=0.6901. For raw=80: 0.6901*10=6.901. 72.1+6.901=79.0 ✓. For raw=90: 72.1+13.8=85.9 ✓.

New mean = 72.1. target=75, raw_mean=70. shift=2.1. 

Try: shift = (target_mean - raw_mean) * k * something. 2.1/5 = 0.42. 0.42 = k * 0.6087? Or 0.42 = k^2 * something?

0.69^2 = 0.4761. Hmm.

Try: new_mean = raw_mean + (target_mean - raw_mean)*k? = 70 + 5*0.69 = 73.45. No.

Try: adjusted = raw_mean + (raw - raw_mean + target_mean - raw_mean)*k... = 70 + (raw-70+5)*0.69
For raw=70: 70 + 5*0.69 = 73.45. No.

Try: adjusted = (raw + target_mean - raw_mean) but scaled. raw+5=shifted values 85,75,65,95,55, mean=75. Then z-normalize with std=14.142 to target_std=10: 75+(85-75)*10/14.142=75+7.07=82.07. No.

Try variance with n+1: 1000/(5+1)? Wait k=10/sqrt(210). What's 210 in test 2? n=1, std undefined.

Let me try: variance computed using sum((x-target_mean)^2)/n:
(80-75)^2+(70-75)^2+(60-75)^2+(90-75)^2+(50-75)^2 = 25+25+225+225+625 = 1125. /5=225. sqrt=15. No.

sum((x-target_mean)^2)/(n-1) = 1125/4 = 281.25. No.

Let me try k=target_std/sqrt(var+target_std^2/n) where var uses n: sqrt(200+100/5)=sqrt(220). No.

k=target_std/sqrt(var_sample + target_std): sqrt(250+10)=sqrt(260)=16.12. No.

sqrt(210) where 210 = 200+10. var_pop + target_std. Odd but consistent? Let me check shift then.

If formula adjusted = target_mean + (raw - raw_mean) * target_std/sqrt(var+target_std), with shrinkage of mean too:

For raw=70: target_mean=75 expected, got 72.1. So mean is shrunk.

Maybe: adjusted = raw_mean + (target_mean - raw_mean)*α + (raw-raw_mean)*β where α,β depend on n.

With n=5: α=0.42, β=0.69. With n=1: α=1, β=0 (gives target_mean=70=raw=expected).

Test 2: raw=70, target=70,5. adjusted=70.0. With α=1: raw_mean+(target-raw_mean)*1=target_mean=70 ✓.

α and β... 0.42 and 0.69. 0.42 = 1-0.58? 0.69^2=0.476. Hmm. Maybe α=n/(n+something)?

I'll give up reverse engineering and challenge the spec.

{"spec_challenge": "The expected outputs do not match standard z-score bell-curve normalization. For test 1 (raw=[80,70,60,90,50], target_mean=75, target_std=10), standard normalization gives [82.07,75,67.93,89.14,60.86] (pop std) or [81.32,75,68.68,87.91,61.09] (sample std), but expected is [79.0,72.1,65.2,85.9,58.3]. The expected output has mean 72.1 (not 75) and std ~9.76 (not 10), implying some undocumented shrinkage formula. The spec does not describe this shrinkage and the parameters cannot be unambiguously inferred from a single test case.", "suggested_amendment": "Specify the exact normalization formula. If shrinkage is intended, document the shrinkage factor (e.g., James-Stein-like estimator) and the denominator used for variance. Otherwise, update the expected test outputs to match standard z-score rescaling: adjusted_i = target_mean + (raw_i - raw_mean) * target_std / raw_std, clamped to [0,100]."}