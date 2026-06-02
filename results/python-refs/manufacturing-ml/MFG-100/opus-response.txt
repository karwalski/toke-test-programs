Let me check the expected values.

For A,1: values [5,6,5]. mean(y^2) = (25+36+25)/3 = 86/3 ≈ 28.667. -10*log10(28.667) = -14.57 → -14.6. Expected -15.4.

Let me try: -10*log10(sum(y^2)) = -10*log10(86) = -19.34. No.

Try RMS: sqrt(mean(y^2)) = sqrt(28.667) = 5.354. -20*log10(5.354) = -14.58. Same.

Try using sample variance formula somehow. mean = 16/3 = 5.333. Maybe -10*log10(mean^2 + var)?

Try: -10*log10(mean(y)^2 + var). var(sample) = ((5-5.333)^2+(6-5.333)^2+(5-5.333)^2)/2 = (0.111+0.444+0.111)/2 = 0.333. mean^2 = 28.444. sum = 28.778. -10*log10(28.778) = -14.59. No.

For A,2: [3,4,3]. expected -10.7. mean(y^2) = (9+16+9)/3 = 34/3 = 11.333. -10*log10(11.333) = -10.54 → -10.5. Expected -10.7.

Diff is about 0.2. Try -10*log10(sum(y^2)/(n-1)): A,2: 34/2=17, -10*log10(17)=-12.3. No.

Try with n in denom different... -10*log10((sum y^2)/n) we did. What if it's mean of y plus something?

A,1: need 10^1.54 = 34.67. Hmm 34.67. sum y^2 = 86, /something = 34.67 → 86/2.48. Not clean.

A,2 need 10^1.07 = 11.75. sum y^2 = 34, /2.894. 

A,1: 34.67 vs mean_sq 28.67, diff 6. mean^2 = 28.44, so 34.67 - 28.44 = 6.23. 
A,2: 11.75 vs mean_sq 11.33, diff 0.42. mean = 10/3 = 3.333, mean^2 = 11.11, 11.75-11.11 = 0.64.

Try: -10*log10(mean^2 + var) where var is population: A,1: var_pop = 0.222. 28.44+0.222=28.67 = mean_sq. Same thing.

Try mean^2 + sample_var: A,1: 28.444 + 0.333 = 28.778. -14.59. No.

What about using stdev not variance? A,1: sd_sample = 0.577. mean^2 + sd = 29.02. No.

Let me check B,1 [4,5,4]: expected -12.7. mean(y^2) = (16+25+16)/3 = 57/3 = 19. -10*log10(19) = -12.79 → -12.8. Expected -12.7. Off by 0.1.

Hmm, B,1 off by 0.1, A,1 off by 0.8. Different errors. Let me reconsider.

Wait: -10*log10(19) = -12.7875, rounds to -12.8 with banker's? Python round(-12.7875, 1) = -12.8. But Python's round uses banker's rounding... actually -12.79 rounds to -12.8. Expected -12.7.

Maybe they truncate or use different rounding. -12.78 truncated to 1 decimal = -12.7. 

A,1: -10*log10(28.667) = -14.5757. Truncate to -14.5. Expected -15.4. Not match.

Let me try MSD = sum(y^2)/n for smaller. A,1 = 28.67, -10log = -14.58. 

Maybe formula uses -10*log10(s^2 + mean^2)? Already tried.

What if larger-is-better formula was applied? -10*log10(mean(1/y^2)). A,1: (1/25+1/36+1/25)/3 = (0.04+0.0278+0.04)/3 = 0.0359. -10*log10 = 14.45. Sign wrong.

A,1 expected -15.4 → 10^1.54 = 34.67. 
A,2 expected -10.7 → 10^1.07 = 11.75.
B,1 expected -12.7 → 10^1.27 = 18.62.
B,2 expected -12.7 → 18.62. B,2 = [4,5,4] same as B,1. Good.

A,1 [5,6,5]: 34.67. sum=16, sum^2/n = 256/3=85.3, no. 
B,1 [4,5,4]: 18.62. sum=13, sum^2 = 169. 
A,2 [3,4,3]: 11.75. sum=10, sum^2=100.

For A,2: 11.75 *3 = 35.25. sum y^2 = 34. +1.25? 
For B,1: 18.62*3 = 55.86. sum y^2 = 57. -1.14?
Hmm inconsistent.

Try sum(y^2)/(n-1): A,1: 86/2=43, log=-16.3. A,2: 34/2=17, -12.3. No.

Try variance formula: -10*log10(var_pop + something)... A,1 var_pop = ((5-5.33)^2*2+(6-5.33)^2)/3 = (0.222+0.444)/3=0.222. 

A,1 target 34.67. 34.67/28.67 = 1.21. Strange.

Hmm let me check: maybe quality_type comes with extra space/whitespace. The values look like the smaller-better formula is right with slightly different computation. Let me check expected -15.4 more carefully. 

10^1.54 = 34.67. What gives 34.67 from [5,6,5]? 5*6 + 5 = 35. (5+6+5)^2/? = 256/?. 

What about: mean^2 * (1 + 3*var/mean^2) approx for nominal... 

Actually let me try: SN = -10*log10(mean(y)^2 + s^2) where s^2 = sample variance:
A,1: mean=5.333, mean^2=28.444, s^2 = ((5-5.333)^2+(6-5.333)^2+(5-5.333)^2)/2 = 0.667/2 wait. (0.111+0.444+0.111)/2 = 0.666/2 = 0.333. Sum = 28.778. log=-14.6. No.

Try sum(y^2)/(n-1) hmm let me think differently. 

What if the formula they use has a typo and it's -10*log10(sum(y^2))? 
A,1: -10*log10(86) = -19.34. No.

What if it includes n in numerator? -10*log10(n*sum(y^2)/something)?

A,1 target 34.67. A,2 target 11.75. B,1 target 18.62.
A,1 sum_y2=86, A,2 sum_y2=34, B,1 sum_y2=57.
86/34.67 = 2.481. 34/11.75 = 2.894. 57/18.62 = 3.061. Not constant.

Maybe it's MSD with sample stdev or stdev included:
MSD = (sum(y-target)^2)/n where target=0 for smaller. That's mean(y^2). Same.

What if there's an off-by-one and they use n+1?
A,1: 86/(3+1)=21.5, -10log=-13.3. No.

What if -10*log10((sum y)^2 /n^2 + (sum (y-mean)^2)/(n-1))?
A,1: mean^2 + sample_var = 28.444 + 0.333 = 28.778. -14.59. No.

A,1: 34.67. 34.67 = 5.333^2 + 6.222 = 6.222 extra. 
A,2: 11.75 = 3.333^2 + 0.639. 
B,1: 18.62 = 4.333^2 + (-0.158). negative makes no sense.

Hmm B,1 actually < mean^2*1 + buffer. mean^2 = 18.778. 18.62 < 18.778. So actually closer to mean^2.

Let me recompute. B,1 = [4,5,4], mean = 13/3 = 4.3333. mean^2 = 18.778. -10*log10(18.778) = -12.74. Rounds to -12.7! 

A,2 = [3,4,3], mean = 10/3 = 3.333. mean^2 = 11.111. -10*log10(11.111) = -10.46. Rounds to -10.5. Expected -10.7.

Hmm not mean^2 either.

A,1 mean^2 = 28.444, -10log = -14.54 → -14.5. Expected -15.4.

What's the formula? Let me try: -10*log10(MSD) where MSD = (1/n) * sum((y-target)^2) and target = mean?
That's just population variance. A,1: var_pop = 0.222. -10log=6.5. No.

Try -20*log10(mean): 
A,1: -20*log10(5.333) = -14.54. -14.5. No, expected -15.4.

Hmm. -10*log10(?):
A,1 target ratio 34.67
A,2 target 11.75  
B,1 target 18.62

A,1: 34.67 - 28.44 = 6.22. var_pop * 28? No, var_pop=0.222.
A,1: variance sample = 0.333. mean^2 * (1 + 3*0.333/28.44) = 28.444 + 1 = ish? 28.78.

Let me try: -10*log10(mean^2 + (n-1)*var_sample) :
A,1: 28.44 + 2*0.333 = 29.11. -14.6.

Let me try -10*log10(sum(y)^2/n):
A,1: 16^2/3 = 85.33. -19.3. No.

-10*log10(sum(y^2 + 1)/n):
A,1: (26+37+26)/3 = 89/3 = 29.67. -14.7. No.

Hmm. Let me reconsider. Maybe expected output has issues or uses a different log base?

ln based? -10/ln(10) * ln(...): same as log10.

Try natural log * some factor:
A,1: target_log_arg such that 10*log10 of it = 15.4 → arg = 34.67.
What's sum y^2 manipulation? 86 - 51.33 = 34.67. 51.33 = ?

OK trying: 10*log10(mean^2/var_sample)... nominal formula
A,1: 28.444/0.333 = 85.33. 10log=19.3. Sign... -10*log10(var/mean^2)? = -19.3.

Mu^2 - sigma^2?
A,1: 28.444 - 0.333 = 28.11. No.

Try -10*log10(sum(y^2)/(n-1)) with n-1:
A,1: 86/2 = 43. -16.3. No.

Hmm, none matching 34.67. Let me try y+1 transformation or y squared differently.

What if values are [5,6,5] but read wrong? Like '5;6;5' could be parsed with semicolons - they are.

What if expected uses some specific Taguchi MSD with different denom?
MSD_smaller = sum(y_i^2)/n  →  Standard.

What about (sum(y_i)^2 + (n-1)*s^2)/n?
A,1: (16^2 + 2*0.333)/3 = (256.667)/3 = 85.56. -19.3. No.

Let me try: -10*log10(mean^2) - 10*log10(1 + cv^2) where cv = std/mean:
A,1: cv^2 = 0.333/28.44 = 0.0117. log10(1.0117) = 0.00505. -10*log = 28.44... -10*log10(28.44*1.0117) = -10*log10(28.78) = -14.59. Same.

Let me check if perhaps they want -10*log10(s^2) instead?
A,1: s^2 = 0.333. log10 = -0.477. -10*log = 4.77. No.

Hmm, expected is -15.4 for A,1, more negative than the standard. What makes it more negative? Larger MSD.

Maybe sum of squares without dividing:
A,1: 86. -