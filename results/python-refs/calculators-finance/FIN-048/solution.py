# Test 1: samples [5,7,8,9,6] mean=7, [3,4,5,6,4] mean=4.4
# var1 = ((5-7)^2+(7-7)^2+(8-7)^2+(9-7)^2+(6-7)^2)/4 = (4+0+1+4+1)/4 = 10/4 = 2.5
# var2 = ((3-4.4)^2+(4-4.4)^2+(5-4.4)^2+(6-4.4)^2+(4-4.4)^2)/4 = (1.96+0.16+0.36+2.56+0.16)/4 = 5.2/4 = 1.3
# pooled = (4*2.5+4*1.3)/8 = 15.2/8 = 1.9
# se = sqrt(1.9*(0.2+0.2)) = sqrt(0.76) = 0.8717
# t = 2.6/0.8717 = 2.9824
# Expected 3.1623. That's sqrt(10) = 3.16227...
# 2.6/sqrt(0.6760) = 3.1623... so denominator should be sqrt(0.676)
# Try se = sqrt(pooled_var/n1 + pooled_var/n2) but with n instead of variance differently
# Actually sqrt(0.676) - what gives that? 
# If we use population variance (divide by n): var1=2.0, var2=1.04
# pooled with (n-1) weights still uses sample var. Let me try: 
# Use variance dividing by n: var1=10/5=2, var2=5.2/5=1.04
# pooled = (5*2+5*1.04)/(10) = 15.2/10 = 1.52... se=sqrt(1.52*0.4)=sqrt(0.608)=0.7797, t=3.334 no
# Try: pooled = (n1*var1+n2*var2)/(n1+n2-2) with sample var:
# = (5*2.5+5*1.3)/8 = 19/8 = 2.375, se=sqrt(2.375*0.4)=sqrt(0.95)=0.9747, t=2.667 no
# Try Welch-like: se = sqrt(var1/n1+var2/n2) = sqrt(0.5+0.26)=sqrt(0.76)=0.8717 same
# Try: se=sqrt((var1+var2)/n) with n=5: sqrt(3.8/5)=sqrt(0.76) same
# What gives 0.676? 2.6^2/10 = 0.676. So denominator squared = 0.676
# pooled_var*(1/n1+1/n2) where pooled_var=1.69, that's (sum of squared dev)/something
# sum_sq1=10, sum_sq2=5.2, total=15.2. 15.2/? = 1.69 -> ?=9. n1+n2-1=9!
# So pooled = (SS1+SS2)/(n1+n2-1), with SS = sum((x-mean)^2)
# Check test 2: [12..20] mean=16, SS1=16+4+0+4+16=40
# [11..19] mean=15, SS2 same=40. Total=80. /9 = 8.889
# se=sqrt(8.889*0.4)=sqrt(3.5556)=1.8856, t=1/1.8856=0.5303. Expected 0.4472=1/sqrt(5)
# 1/sqrt(5)=0.4472, so se^2=5, se=sqrt(5)
# pooled*(0.4)=5 -> pooled=12.5. SS_total/pooled = 80/12.5=6.4. Hmm
# Test1: se^2=0.676, pooled*0.4=0.676 -> pooled=1.69. SS/1.69=15.2/1.69=8.99≈9
# Test2: 80/12.5=6.4. Not consistent.
# Wait test2 expected 0.4472. Let me recompute. mean1=16,mean2=15, diff=1
# t=1/se=0.4472 -> se=2.236=sqrt(5)
# What formula? se=sqrt(pooled*(1/n1+1/n2)), pooled*(2/5)=5, pooled=12.5
# SS1+SS2=80. 80/(n1+n2-2)=80/8=10. se=sqrt(10*0.4)=2. t=0.5
# Hmm. 80/?=12.5 -> ?=6.4
# Maybe formula: t = (m1-m2)/sqrt(var1/n1+var2/n2) but using something else
# Test2: var1=20, var2=20 (sample). var1/n1+var2/n2=4+4=8, sqrt=2.828, t=0.3536 no
# Pop var: var1=16,var2=16. 16/5+16/5=6.4, sqrt=2.5298, t=0.3953 no
# Hmm. What if se = sqrt(var1+var2) where var uses sample (n-1)?
# Test1: sqrt(2.5+1.3)=sqrt(3.8)=1.949, t=1.334 no
# What about Cohen's d or something else? 
# Expected 3.1623 = sqrt(10). Diff=2.6, so 2.6/sqrt(10)*... no 2.6=sqrt(6.76), sqrt(10)*?=2.6/3.1623... 
# Actually maybe answer = (m1-m2)*sqrt(n)/sqrt(pooled_sample_var) for paired-like?
# Test1: 2.6*sqrt(5)/sqrt(1.9) = 2.6*2.236/1.378=4.218 no
# Try: t with se = sqrt((SS1+SS2)/(n1*n2))... 15.2/25=0.608, sqrt=0.7797, t=3.334 no
# Try: pooled std dev s_p, then t=(m1-m2)/(s_p*sqrt(2/n))
# Same as before since n1=n2. Already computed = 2.9824
# Hmm. Let me try simple: t = (m1-m2)/sqrt((var1+var2)/n) where var=sample, n=n1=n2
# Test1: sqrt(3.8/5)=sqrt(0.76)=0.8717, t=2.9824. Same.
# t = (m1-m2)/sqrt((var1+var2)/(n-1))? Test1: sqrt(3.8/4)=0.9747, t=2.667 no
# Let me check: expected 3.1623 for test1, 0.4472 for test2
# Ratio: 3.1623/0.4472 = 7.071 = 5*sqrt(2)
# Diff ratio: 2.6/1 = 2.6
# se ratio: should be 2.6/7.071 = 0.3677
# Test1 se = X, Test2 se = X/0.3677 = 2.72X
# Test1: SS=15.2, Test2: SS=80. Ratio 80/15.2=5.263
# If se = c*sqrt(SS), ratio = sqrt(5.263)=2.294. Not matching.
# Test1 se=2.6/3.1623=0.8222, Test2 se=1/0.4472=2.2361
# se^2: 0.6760, 5.0
# Hmm, 0.676 = 15.2 * 0.04445... 5 = 80 * 0.0625
# 0.04445 = 1/22.5? 22.5=? 
# Let me try: se^2 = SS_total/(n1*n2*(n1+n2-2)/something)
# Test1: 15.2/X=0.676 -> X=22.485
# Test2: 80/X=5 -> X=16
# Not consistent ratios. Weird.
# Wait, maybe I should just compute what formula gives those exact values
# Test1: t=sqrt(10)=3.16228. Test2: t=1/sqrt(5)=0.44721
# Test1 t^2 = 10. (m1-m2)^2/se^2=10 -> 6.76/se^2=10 -> se^2=0.676
# Test2 t^2=0.2. 1/se^2=0.2 -> se^2=5
# Look: 0.676 = 6.76/10. And 6.76 = (m1-m2)^2. Test2: 1=(m1-m2)^2, 1/0.2=5
# se^2 = (m1-m2)^2/t^2 -- circular
# Try: se^2 = SS_within / (n1+n2)... Test1: 15.2/10=1.52 no
# se^2 = (SS1/n1 + SS2/n2)... Test1: 10/5+5.2/5=2+1.04=3.04 no
# se^2 = (SS1/n1^2 + SS2/n2^2)... Test1: 10/25+5.2/25=0.608 no
# Hmm what gives 0.676 for test1 and 5 for test2?
# 0.676 = 0.4 * 1.69. 1.69 = 15.2/9 (n1+n2-1)
# 5 = 0.4 * 12.5. 12.5 = 80/6.4. 6.4=? 
# Hmm, 0.676 and 5... 5/0.676 = 7.396
# Different approach: maybe pooled_var uses N (not n-1) in numerator weights:
# pooled = (n1*var1_sample + n2*var2_sample)/(n1+n2-2)
# Test1: (5*2.5+5*1.3)/8 = 19/8 = 2.375
# se=sqrt(2.375*0.4)=sqrt(0.95), t=2.667. No.
# Maybe answer simply uses different normalization. Let me check
# what if the formula is t-stat using std error of mean of differences treating as paired?
# Test1: diffs = [2,3,3,3,2], mean=2.6, var=(0.36+0.16+0.16+0.16+0.36)/4=1.2/4=0.3
# se=sqrt(0.3/5)=sqrt(0.06)=0.2449, t=2.6/0.2449=10.614 no
# What about diffs uncorrected: var=0.3*4/5=0.24, se=sqrt(0.24/5)=0.219, t=11.87 no
# Hmm. Test2 paired: diffs all 1, var=0, undefined. So not paired.
# Let me try z-test style: se=sqrt(var1/n1+var2/n2) with pop var (/n)
# Test1: var1=2, var2=1.04, se=sqrt(2/5+1.04/5)=sqrt(0.608)=0.7797, t=3.334 no
# With sample var and dividing by n-1 in se denom:
# se=sqrt(var1/(n1-1)+var2/(n2-1))? Test1: sqrt(2.5/4+1.3/4)=sqrt(0.95)=0.9747, t=2.667 no
# t = (m1-m2)*sqrt(n1*n2/(n1+n2))/s_pooled  where s_pooled=sqrt(SS_total/(n1+n2-2))
# Same as standard. =2.9824
# I'm stuck. Let me check if expected might use n in denominator of variance and not n-1
# pooled var with /n variances: var1=2,var2=1.04. 
# pooled=(n1*var1+n2*var2)/(n1+n2) = 15.2/10=1.52, se=sqrt(1.52*0.4)=0.7797, t=3.334
# Or pooled=(n1*var1+n2*var2)/(n1+n2-2)=15.2/8=1.9, se=sqrt(1.9*0.4)=0.8717, t=2.9824 same as original
# Hmm. What about: t = (m1-m2)/sqrt(var_pooled*2/n) where var_pooled = (var1+var2)/2
# Test1 sample var: (2.5+1.3)/2=1.9, se=sqrt(1.9*2/5)=sqrt(0.76)=0.8717, t=2.9824 same
# Test2: var1=var2=20, pooled=20, se=sqrt(20*2/5)=sqrt(8)=2.828, t=1/2.828=0.3536 no
# But expected test2 = 0.