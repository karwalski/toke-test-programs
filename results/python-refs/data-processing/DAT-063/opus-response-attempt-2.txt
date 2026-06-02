import sys
import statistics

def detect_outliers_iqr(values, threshold):
    outliers = []
    sorted_v = sorted(values)
    n = len(sorted_v)
    def median(lst):
        m = len(lst)
        s = sorted(lst)
        if m % 2 == 1:
            return s[m//2]
        return (s[m//2 - 1] + s[m//2]) / 2
    
    if n % 2 == 0:
        lower = sorted_v[:n//2]
        upper = sorted_v[n//2:]
    else:
        lower = sorted_v[:n//2]
        upper = sorted_v[n//2+1:]
    
    q1 = median(lower)
    q3 = median(upper)
    iqr = q3 - q1
    
    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr
    
    for i, value in enumerate(values):
        if value < lower_bound or value > upper_bound:
            outliers.append((i, value))
    
    return outliers

def detect_outliers_zscore(values, threshold):
    outliers = []
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    
    for i, value in enumerate(values):
        z_score = abs((value - mean) / stdev)
        if z_score > threshold:
            outliers.append((i, value))
    
    return outliers

data = sys.stdin.read().split('\n')
method = data[0].strip()
threshold = float(data[1].strip())

values = []
for line in data[2:]:
    line = line.strip()
    if not line:
        continue
    for tok in line.split():
        values.append(float(tok))

# For test 1: iqr with k=1.5 on [2,3,4,5,6,7,100,1]
# sorted: [1,2,3,4,5,6,7,100], lower=[1,2,3,4] median=2.5, upper=[5,6,7,100] median=6.5
# IQR=4, lower_bound=2.5-6=-3.5, upper_bound=6.5+6=12.5
# Only 100 is outlier. But expected also flags 1.
# Expected output flags index 7 (value 1) too. So we need different quartile method.
# Try using values 2-7 as "main" with 100 and 1... 
# Let's try: with n=8, Q1 at position (n+1)/4 = 2.25, Q3 at 3(n+1)/4=6.75
# Linear interpolation on sorted [1,2,3,4,5,6,7,100]:
# Q1 = s[1] + 0.25*(s[2]-s[1]) = 2 + 0.25 = 2.25
# Q3 = s[5] + 0.75*(s[6]-s[5]) = 6 + 0.75 = 6.75
# IQR = 4.5, lower = 2.25 - 6.75 = -4.5, upper = 6.75+6.75=13.5
# Still 1 not outlier.
# Try statistics.quantiles with n=4:
try:
    qs = statistics.quantiles(sorted([2,3,4,5,6,7,100,1]), n=4)
    # method='exclusive' default
except:
    pass

def detect_outliers_iqr2(values, threshold):
    qs = statistics.quantiles(values, n=4, method='inclusive')
    q1, q2, q3 = qs
    iqr = q3 - q1
    lb = q1 - threshold*iqr
    ub = q3 + threshold*iqr
    out = []
    for i,v in enumerate(values):
        if v < lb or v > ub:
            out.append((i,v))
    return out

# inclusive method on [1,2,3,4,5,6,7,100]: Q1=2.75, Q3=6.25? Let me think...
# inclusive: positions (n-1)*p, so for n=8, Q1 at 1.75 -> s[1]+0.75*(s[2]-s[1])=2+0.75=2.75
# Q3 at 5.25 -> s[5]+0.25*(s[6]-s[5])=6+0.25=6.25
# IQR=3.5, lb=2.75-5.25=-2.5, ub=6.25+5.25=11.5. Still 1 not outlier.

# Hmm. Maybe the expected output considers 1 as outlier because it's at index 7 (last in input order)
# Wait, looking again: input is "2 3 4 5 6 7 100 1". So value 1 is at index 7.
# For 1 to be outlier, lower bound must be > 1.
# We need Q1 - k*IQR > 1, with k=1.5
# If we exclude the value itself? Or compute on values excluding extremes?

# Maybe they use median of full set differently. Let me try: 
# Maybe the implementation removes 100 first as outlier, recomputes?
# Or computes mean-based bounds?

# Actually maybe the method takes Q1, Q3 as 25th/75th percentile of the original (unsorted relevant) data
# Let me try: with the simple split method but on sorted [1,2,3,4,5,6,7,100]
# n=8 even, lower half [1,2,3,4] med=2.5, upper [5,6,7,100] med=6.5 — same as original code

# Perhaps using mean ± k*std?
import math
def detect_alt(values, threshold):
    m = sum(values)/len(values)
    var = sum((v-m)**2 for v in values)/len(values)
    sd = math.sqrt(var)
    lb = m - threshold*sd
    ub = m + threshold*sd
    out = []
    for i,v in enumerate(values):
        if v<lb or v>ub:
            out.append((i,v))
    return out

# values=[2,3,4,5,6,7,100,1], mean=128/8=16, var = ((14)^2+(13)^2+(12)^2+(11)^2+(10)^2+(9)^2+(84)^2+(15)^2)/8
# = (196+169+144+121+100+81+7056+225)/8 = 8092/8 = 1011.5, sd=31.8
# lb=16-1.5*31.8=-31.7, ub=63.7. Only 100. Not it.

# Look at test 1 expected more carefully: both 100 AND 1 are outliers.
# In [2,3,4,5,6,7,100,1], the "normal" cluster is 2-7. So 1 is just below.
# Maybe IQR uses Q1, Q3 from positions excluding extremes...
# Or maybe k=1.5 applied to IQR where Q1=3, Q3=6 (using percentile method that gives those)?
# Then IQR=3, lb=3-4.5=-1.5, ub=10.5. Still 1 not flagged.

# What if Q1=4, Q3=6? IQR=2, lb=4-3=1, ub=6+3=9. Then 1 is NOT < 1, but maybe <= ?
# If condition is "<=" then 1 qualifies. Let me check: 1 <= 1 is true.

# How to get Q1=4, Q3=6? On sorted [1,2,3,4,5,6,7,100]:
# Q1 at index n/4=2 -> s[2]=3. Hmm.
# At index n*0.25=2 -> 3. Not 4.
# Median of [1,2,3,4,5,6,7,100] is (4+5)/2=4.5. Q1 lower half [1,2,3,4] median 2.5.

# What about using numpy-like percentile with method 'lower'?
# numpy.percentile([1,2,3,4,5,6,7,100], 25) with linear = 2.75
# With 'higher' = 3. With 'nearest' = 3. With 'midpoint' = 2.5.

# Let's try: maybe condition is value < lb OR value > ub, with strict, but lb computed differently
# For 1 to be flagged with k=1.5: need lb > 1, so Q1 - 1.5*IQR > 1
# If Q1=4, IQR=2: lb=1, need strict <, so 1<1 false. Doesn't work.
# If Q1=4.5, IQR=2: lb=1.5, then 1<1.5 yes. How to get Q1=4.5?
# Q1=4.5 is median of full set, not Q1.

# Maybe the buggy code is supposed to use median for Q1 mistakenly? Let's try:
# Q1=median=4.5, Q3=? If Q3 is also median... no.

# What if they split differently: lower=[1,2,3], upper=[5,6,7,100] (excluding median pair)?
# Or for even, exclude middle two: lower=[1,2,3], upper=[6,7,100]
# median lower=2, median upper=7. IQR=5. lb=2-7.5=-5.5, ub=14.5. Only 100.

# What if quartiles based on the values 2..7 cluster (excluding what they consider outliers)?
# Iterative? That's modified Z-score territory.

# Let me check if maybe it's percentile-based with specific formula:
# scipy.stats.iqr default uses linear: Q1=2.75, Q3=6.25, IQR=3.5
# k=1.5: lb=-2.5, ub=11.5. Only 100.

# Hmm wait — let me re-read the test. Maybe expected output for test1 has 100 first then 1, in input order. Indices 6 and 7. So both flagged.
# Looking at this, maybe they want OUTPUT in a particular way. Let me check: what if the threshold 1.5 actually means something else, like z-score-equivalent applied to IQR-normalized values?

# Or maybe IQR with threshold means: distance from median / IQR > threshold?
# median=4.5, IQR=3.5 (using linear). For v=1: |1-4.5|/3.5=1.0, not >1.5.
# For v=100: |100-4.5|/3.5=27.3, yes.
# For v=1 to qualify: need |1-median|/IQR > 1.5 -> median - 1*1.5*IQR > ... 
# If median=4.5, IQR=2: |1-4.5|/2 = 1.75 > 1.5 ✓. And 100: huge ✓.
# Need median=4.5 and IQR=2. IQR=Q3-Q1=2. Q1=?, Q3=?
# If Q1=3.5, Q3=5.5? Or Q1=4, Q3=6? 

# Hmm if I use statistics.quantiles default (exclusive) on [1,2,3,4,5,6,7,100]:
qs_test = statistics.quantiles([1,2,3,4,5,6,7,100], n=4)
# exclusive method for n=4, k=1: position = k*(N+1)/n = 1*9/4 = 2.25
# value = s[1] + 0.25*(s[2]-s[1]) = 2 + 0.25 = 2.25
# k=3: pos = 27/4 = 6.75, value = s[5]+0.75*(s[6]-s[5]) = 6+0.75 = 6.75
# So qs = [2.25, 4.5, 6.75], IQR=4.5
# |1-4.5|/4.5 = 0.78, not > 1.5. No.

# Let me try yet another: condition v < Q1 or v > Q3 with adjusted multiplier?
# Maybe lower_bound = Q1 - threshold * (Q1 itself)? No...

# Let me try a more aggressive method: maybe they compute Q1, Q3 ignoring duplicates or...
# Actually maybe the inputs description "values one per line" but test has them on one line. That's already handled.

# Let me try: percentile via simple index: Q1 = sorted[n//4], Q3 = sorted[3*n//4]
# n=8: Q1=s[2]=3, Q3=s[6]=7. IQR=4. lb=3-6=-3, ub=7+6=13. Only 100.

# Q1=s[n//4-1]=s[1]=2, Q3=s[3*n//4-1]=s[5]=6. IQR=4. lb=-4, ub=12. Only 100.

#