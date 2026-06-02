# Test 1: simple=2.60 means after year 2, cumulative=7000, need 3000 more from year 3's 5000 = 0.6
# Test 1 discounted: expected 3.15
# Year 1: 3000/1.1 = 2727.27, cum=2727.27
# Year 2: 4000/1.21 = 3305.79, cum=6033.06
# Year 3: 5000/1.331 = 3756.57, cum=9789.63
# Year 4: 6000/1.4641 = 4098.08, cum=13887.71
# Need 10000, after year 3: 9789.63, remaining 210.37 / 4098.08 = 0.0513 -> 3.05
# But expected is 3.15. Hmm.
# Maybe they index starting differently. If we treat year as i (0-indexed start)
# Or maybe the fractional part uses simple cash flow not discounted
# remaining 210.37 / 6000 (undiscounted year 4 cf) = 0.035 -> no
# Try: discount year starts at 0? Year 0: 3000, Year 1: 4000/1.1=3636.36, Year 2: 5000/1.21=4132.23
# cum after year 0: 3000, year 1: 6636.36, year 2: 10768.60 -> payback in year 2
# remaining = 10000 - 6636.36 = 3363.64 / 4132.23 = 0.814 -> 2.81 no
# 
# Test 2: simple = 2.50: cum after 2 = 4000, need 1000/2000 = 0.5 ✓
# Test 2 discounted expected 2.72
# Year 1: 2000/1.05=1904.76, Year 2: 2000/1.1025=1814.06, cum=3718.82
# Year 3: 2000/1.157625=1727.68, cum=5446.50
# need 5000, after year 2: 3718.82, remaining 1281.18 / 1727.68 = 0.7415 -> 2.74
# Expected 2.72. Close but not exact.
# 
# Maybe they use remaining/undiscounted: 1281.18/2000 = 0.64 -> 2.64 no
# 
# Try discounting starting year=0: Year 0: 2000, Year 1: 2000/1.05=1904.76, Year 2: 2000/1.1025=1814.06
# cum: 2000, 3904.76, 5718.82 -> in year 2, remaining=5000-3904.76=1095.24/1814.06=0.6037 -> 2.60 no
#
# Try: simple payback fraction computed differently for discounted - use the discounted of NEXT year but year index from 1
# What if formula is: years_before + remaining_undiscounted/cash_flow_that_year, but discount applied to remaining?
# 
# Test 2: after year 2 discounted cum=3718.82. remaining = 5000-3718.82 = 1281.18
# 1281.18 / 1727.68 = 0.7415... -> 2.74
# Expected 2.72. 
#
# Hmm let me try: remaining/(cash_flow/(1+r)^(year)) where year is the fractional year?
# Or maybe they include partial-year discounting iteratively
# 
# Let me try test 1 more carefully with different formula:
# What if remaining = initial - cum_discounted, fraction = remaining / cash_flow_undiscounted?
# Test 1: 10000-9789.63=210.37/6000=0.035 -> 3.04, no
# 
# What if it's: fraction = remaining_undiscounted / cf_undiscounted, where cum tracked undiscounted but check vs discounted threshold?
# 
# Let me try: maybe discount rate applies to investment growing?
# initial * (1+r)^year compared to cumulative cash flow
# Test 1: 10000*1.1=11000 vs 3000 -> no
# 10000*1.21=12100 vs 7000 -> no  
# 10000*1.331=13310 vs 12000 -> no
# 10000*1.4641=14641 vs 18000 -> in year 4
# remaining = 14641-12000=2641/6000=0.44 -> 3.44 no
#
# Try future value comparison: cum_cf vs initial*(1+r)^year
# Hmm let me try year indexing from 0 for discount:
# Test 1 disc with year starting 0: 3000/1, 4000/1.1=3636.36, 5000/1.21=4132.23, 6000/1.331=4507.89
# cum: 3000, 6636.36, 10768.60 -> year 2 (index)
# remaining=10000-6636.36=3363.64/4132.23=0.814 -> 2.81 no
#
# Test 2 disc year from 0: 2000, 2000/1.05=1904.76, 2000/1.1025=1814.06, 2000/1.157625=1727.68
# cum: 2000, 3904.76, 5718.82 -> at index 2
# remaining=5000-3904.76=1095.24/1814.06=0.6037 -> 2.60, expected 2.72 no
#
# Let me try: 3.15 = 3 + 0.15. What gives 0.15?
# Test 1: 210.37/? = 0.15 -> ? = 1402.47. Hmm. Or maybe different cum.
# Maybe they recompute cum differently. What if cum after year 3 is something giving remaining/cf4 = 0.15?
# 6000/1.4641 = 4098.08 * 0.15 = 614.71. So cum = 10000-614.71 = 9385.29
# Or 6000 * 0.15 = 900, cum=9100
# 
# What if discount applies to remaining as: remaining at year N / cf at year N+1, both at present value
# but "year" is from start of investment
# Wait maybe simple interp method differs. Let me try Test 2 reverse-engineering 2.72:
# 0.72 fraction. cum_before_year3 = X, remaining = 5000-X, cf3_disc = 1727.68
# (5000-X)/1727.68 = 0.72 -> 5000-X=1244, X=3756
# Hmm, 3756 doesn't match 3718.82.
# Try cf3 undiscounted: (5000-X)/2000=0.72 -> X=3560 no
# Try: 0.72 * 2000 = 1440 = remaining undiscounted? cum_undisc = 3560? no, that's 4000 after 2 yrs
# What's (5000-4000)/?=0.72... 1000/0.72=1388.89. 2000/1.05^? = 1388.89, 1.05^?=1.44, ?=7.5. no
#
# Try: remaining = initial - cum_undisc(year n), but fraction uses discounted cf
# Test 2: after year 2 undisc cum = 4000, remaining = 1000. cf3_disc=1727.68
# 1000/1727.68=0.579 -> 2.58 no
#
# Let me look for 0.15 in test1 a different way.
# What if discounted payback uses cumulative undiscounted but compares to discounted investment?
# initial_disc at year n = initial/(1+r)^n
# Year 1: 10000/1.1=9090.91, cum_cf=3000 < 
# Year 2: 10000/1.21=8264.46, cum=7000 < 
# Year 3: 10000/1.331=7513.15, cum=12000 >= ✓
# remaining = 7513.15-7000 = 513.15 / 5000 = 0.103 -> 2.10 no
#
# OK let me try yet another: discounted cash flows but using mid-year or year n-0.5 convention
# Year 1: 3000/1.05 (half year)... getting complicated
#
# Let me check: maybe simple_payback uses fraction with discounted cf for remaining year
# Test 1 simple expected 2.60: after yr2 cum=7000, need 3000. cf3=5000, 3000/5000=0.6 ✓
# Both tests match basic for simple.
#
# Test 1 discounted 3.15: maybe they treat year index as i+1 in different way
# What if fraction = remaining / (cf_n / (1+r)^(n-1)) i.e. discount one less year
# Year 4 cf disc one less: 6000/1.331 = 4507.89
# After year 3 cum: 9789.63, remaining=210.37/4507.89=0.0467 -> 3.05 no
#
# What if cum uses (1+r)^(n-1)?
# Year 1: 3000/1=3000, Year 2: 4000/1.1=3636.36, Year 3: 5000/1.21=4132.23, Year 4: 6000/1.331=4507.89
# cum: 3000, 6636.36, 10768.60 -> year 2 (0-idx)
# remaining = 10000-6636.36=3363.64. /4132.23=0.814 -> 2.81
# /5000=0.673 -> 2.67 no
#
# Hmm. Let me try test 2: 0.72 fraction
# If discount uses year n-1: 2000, 2000/1.05=1904.76, 2000/1.1025=1814.06, 2000/1.157625=1727.68
# cum: 2000, 3904.76, 5718.82, 7446.50
# year 2 (0-idx): remaining 5000-3904.76=1095.24/1814.06=0.6037 -> 2.60 no
#
# Try future value approach: invest grows, compare cum cash flows
# FV of investment at year n = 10000*(1.1)^n
# Year 1: 11000 vs 3000
# Year 2: 12100 vs 7000
# Year 3: 13310 vs 12000
# Year 4: 14641 vs 18000 -> recovered
# remaining at start of year 4 = 14641-12000 = 2641. cf year 4 = 6000
# but FV is changing. Maybe: (14641-12000)/6000 = 0.44 -> 3.44 no
# Or compare: at what fraction f does 10000*1.1^(3+f) = 12000 + 6000*f?
# Try f=0.15: LHS=10000*1.1^3.15=10000*1.331*1.1^0.15=13310*1.01435=13501
#   RHS=12000+900=12900. Not equal.
# f=0.2: LHS=10000*1.1^3.2=13310*1.0192=13565, RHS=13200. closer
# f=0.25: 10000*1.1^3.25=13310*1.0241=13631, RHS=13500
# f=0.3: 13310*1.0290=13696, RHS=13800. crossed
# So somewhere between 0.25-0.3, not 0.15
#
# Let me try the formula where remaining_for_year_n / discounted_cf_n but the year exponent is the resulting fractional year
# Iterative: year = 3 + f, 10000 = sum + 6000/(1.1)^(3+f)?
# sum disc through year 3 = 9789.63
# 6000/(1.1)^(3+f) = 210.37
# (1.1)^(3+f) = 28.52, 3+f = log(28.52)/log(1.1) = 35.1... no way
# 
# Hmm. Maybe I'm miscomputing. Let me try a totally different formula.
# What if "discounted payback" means: time when sum of cf = initial*(1+r)^t (future-valued investment)?
# 12000 + 6000*f = 10000 * (1.1)^(3+f)
# At f=0.15: 12900 vs 10000*1.1^3.15 = 13501. Diff -601
# At f=0.5: 15000 vs 10000*1.1^3.5 = 14049. Diff +951
# At f=0.3: 13800 vs 13696. close, +104
# At f=0.28: 13680 vs 13683. ≈
# So ~0.28, not 0.15
#
# Try: 10000 = sum undisc through n + cf_{n+1}*f, with whole-period discounting
# Test 1: 10000 = 12000... already over. Doesn't fit.
#
# Test 2 expected 2.72. Try various