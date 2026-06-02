# Test 1: window=3, alpha=0.5
# Expected EMA at i=2: 27.50, i=3: 33.75, i=4: 41.88
# Values: 10, 20, 30, 40, 50
# Let's figure out EMA formula
# If EMA starts at first value being SMA of window:
# i=2: SMA=20, that's the first EMA = 20? No, expected 27.50
# Try: EMA seeded with first value (10), then apply alpha each step
# i=0: 10
# i=1: 0.5*20 + 0.5*10 = 15
# i=2: 0.5*30 + 0.5*15 = 22.5  -- but expected 27.50
# Try alpha = 2/(N+1) ignoring given alpha? N=3, alpha=0.5, same
# Try: EMA = alpha*current + (1-alpha)*prev, but prev_ema starts as values[0], advancing differently
# What if EMA uses different init: starts with SMA of first window
# i=2: ema = SMA(10,20,30) = 20
# Hmm not 27.50 either.
# Try: seed ema with first value, but alpha applied differently:
# ema = current * (1-alpha) + prev * alpha? 
# i=0: 10
# i=1: 20*0.5 + 10*0.5 = 15
# Same.
# Try seeding ema = values[window-1] at i=window-1
# i=2: ema = 30 (just current)? Then i=3: 0.5*40+0.5*30 = 35, expected 33.75. No.
# Try: ema seeded at i=0 = values[0], and recompute each step but output only after window
# Test 2: window=2, alpha=0.3, values 5,10,15
# i=1: expected EMA 8.00
# 0.3*10 + 0.7*5 = 3 + 3.5 = 6.5. No.
# 0.3*5 + 0.7*10 = 1.5+7 = 8.5. No.
# Try: ema_0 = values[0]=5, ema_1 = 0.3*10+0.7*5 = 6.5. Expected 8.00.
# Hmm. What if alpha applied to prev: ema = alpha*prev + (1-alpha)*current
# i=1: 0.3*5 + 0.7*10 = 8.5. Close but no.
# What if ema initialized as average of first two? 
# i=1: ema = (5+10)/2 = 7.5. Then i=2: 0.3*15+0.7*7.5=4.5+5.25=9.75. Expected 12.50. No.
# Test 1 expected i=2 EMA = 27.50. Let's reverse engineer:
# i=3: 33.75 = 0.5*40 + 0.5*27.5 ✓
# i=4: 41.88 ≈ 0.5*50 + 0.5*33.75 = 41.875 ✓
# So at i=2, ema=27.5. With values 10,20,30:
# If ema_0 = 10: ema_1 = 0.5*20+0.5*10=15, ema_2=0.5*30+0.5*15=22.5. No.
# If we compute ema only starting at i=window-1, seeded with current value:
# ema_2 = 30? No.
# What gives 27.5 from 10,20,30 with alpha=0.5?
# 27.5 = 0.5*30 + 0.5*25, so prev=25
# 25 = 0.5*20 + 0.5*30, so seed=30? That means ema_0 starts at values[0]... hmm
# Or: ema_1 with values[1]=20 and seed 30: 0.5*20+0.5*30=25, then ema_2=0.5*30+0.5*25=27.5 ✓
# So seed is... 30? That's values[2]. Odd.
# Or maybe EMA iterates from i=0 with seed = WMA of first window or something
# Test 2: ema_1=8.00, values 5,10. alpha=0.3
# 8 = 0.3*10 + 0.7*x => 8-3=5 => x=5/0.7=7.14. Hmm not clean.
# 8 = 0.3*x + 0.7*10 => 0.3x=1 => x=3.33. No.
# Try ema = (1-alpha)*current + alpha*prev:
# 8 = 0.7*10 + 0.3*x => 1 = 0.3x => x=3.33. No.
# 8 = 0.7*x + 0.3*5? => 6.5=0.7x => x=9.28. No.
# Maybe seeded with SMA of full window at position window-1:
# Test2 i=1 (window=2): SMA = 7.5. Then EMA at i=1 = 7.5? No, expected 8.00.
# What if EMA = alpha*current + (1-alpha)*SMA?
# Test2 i=1: 0.3*10 + 0.7*7.5 = 3+5.25=8.25. Close not exact.
# 0.3*7.5+0.7*10=2.25+7=9.25. No.
# Test1 i=2: SMA=20. 0.5*30+0.5*20=25. No, expect 27.5
# Hmm. Let me try: EMA = current * alpha + WMA * (1-alpha)?
# Test1 i=2: WMA=(1*10+2*20+3*30)/6=140/6=23.33. 0.5*30+0.5*23.33=26.67. No.
# Test1 expected 27.5 at i=2. What's 27.5? = 55/2. 
# 0.5*30 + 0.5*25 = 27.5. What's 25? avg(20,30)=25!
# So seed for EMA might be SMA of last (window-1) values?
# Test2 i=1: alpha=0.3. avg(5)=5. 0.3*10+0.7*5=6.5. No.
# Or seed = previous value? 
# Test1 ema_2: alpha*30 + (1-alpha)*prev where prev = avg(values 20,..)? 
# 27.5 = 0.5*30 + 0.5*25. 25 = avg(20,30) but that's the current window
# Maybe EMA iterates differently: ema starts when we have enough data, seeded with SMA
# i=2: ema = SMA(10,20,30) = 20 (seed at start of valid output)
# But expected 27.5 not 20. Unless first output is seed-related.
# Actually re-examining: maybe EMA computed continuously from start with init=values[0], 
# but my formula has prev mishandled. Let me recheck my code's variable `ema` initialization.
# In code: at i=0, ema=values[0]=10. At i=1, ema = 0.5*20+0.5*10 = 15. At i=2: 0.5*30+0.5*15=22.5
# Got 22.50 in actual output. Expected 27.5.
# Difference: 27.5 - 22.5 = 5. 
# Try alpha and (1-alpha) swapped: at i=1: 0.5*10+0.5*20=15 same.
# Try alpha=0.5 means weight on history: ema = (1-alpha)*current + alpha*prev. Same with 0.5.
# Try different init: ema_0 = 2*values[0] = 20? Then i=1: 0.5*20+0.5*20=20, i=2: 0.5*30+0.5*20=25. No.
# Try ema_0 = values[0]+10? Special?
# Let me try: maybe EMA only starts accumulating from i=1 with init values[1]
# Test1: ema_1=20, ema_2=0.5*30+0.5*20=25. No, want 27.5
# Try ema_0=values[0], but skip and use:
# ema_i = current + alpha * (prev - current)? No that's same as (1-alpha)*current+alpha*prev
# Hmm. Let me try: ema = prev + alpha*(current-prev)
# i=0: 10, i=1: 10+0.5*(20-10)=15, i=2: 15+0.5*(30-15)=22.5. Same.
# What if init ema=0?
# i=0: 0.5*10+0.5*0=5, i=1: 0.5*20+0.5*5=12.5, i=2:0.5*30+0.5*12.5=21.25. No.
# What if EMA continues even past the test but I need different formula entirely?
# 27.5, 33.75, 41.88
# 33.75 - 27.5 = 6.25
# 41.875 - 33.75 = 8.125
# 27.5 = ?
# Try: ema = alpha*current + (1-alpha)*prev_ema, with prev_ema at i=window-1 = values[window-1]
# So ema seeded at i=window-1 = values[window-1] (i.e., ema_2 = 30)
# Then output at i=2 is... 30? Not 27.5
# What if we still process from i=0 but seed differently?
# Maybe ema_0 = values[0], and continues with formula but output starts at i=window-1, and we want 27.5 there
# So ema_2 = 27.5. Working back: ema_2 = 0.5*30+0.5*ema_1 => ema_1 = 25
# ema_1 = 0.5*20 + 0.5*ema_0 => ema_0 = 30
# So seed = 30 = values[2]? Or = some other thing. In test 2:
# ema_1=8 = 0.3*10+0.7*ema_0 => ema_0 = 5/0.7 = 7.14... 
# Hmm not clean. Let me try ema = (1-alpha)*current + alpha*prev:
# Test2: ema_1=8 = 0.7*10 + 0.3*ema_0 => ema_0 = 1/0.3 = 3.33. No.
# Test2 ema_1 = 8, ema_2 = 12.10
# 12.10 = ?*15 + ?*8
# If ema = alpha*current + (1-alpha)*prev: 0.3*15+0.7*8 = 4.5+5.6=10.10. No, expected 12.10.
# If ema = (1-alpha)*current + alpha*prev: 0.7*15+0.3*8 = 10.5+2.4=12.9. Close to 12.10 but no.
# Try alpha*current + alpha*prev? 0.3*15+0.3*8 = 6.9. No.
# 12.10 from 15 and 8: 12.10 = 0.82*15 - 0.21 hmm
# Or maybe prev isn't 8. Let me consider ema_1 might be calculated but output is different.
# Actually let me check: what if EMA output is something like cumulative?
# Test2 ema values: 8.00, 12.10
# 12.10 - 8.00 = 4.10
# 8 - ? 
# Try: ema_i = alpha * current + (1-alpha) * prev_ema, but prev_ema for first is 0
# Test2 i=0: 0.3*5+0.7*0 = 1.5
# i=1: 0.3*10+0.7*1.5 = 3+1.05 = 4.05. No.
# Or seed = sum of first window?
# Test2 seed at i=1 = sum(5,10) = 15? Then ema_1 = 15? No expected 8.
# Or seed = values[0] and recurrence different.
# Let me try: SMA-EMA hybrid - EMA reported is alpha*SMA + (1-alpha)*prev_ema_or_seed
# Test1 i=2: SMA=20. ema = 0.5*20 + 0.5*seed. If seed= 35, ema=27.5
# Test1 i=3: SMA=30. ema = 0.5*30 + 0.5*27.5 = 28.75. Expected 33.75. No.
# 33.75 = 0.5*30 + 0.5*37.5 or 0.5*40 + 0.5*27.5 ✓
# So 33.75 = 0.5*40 + 0.5*27.5 means ema_i = 0.5*values[i+1] + 0.5*prev?? Look-ahead?
# Test1 i=2 ema=27.5 = 0.5*values[3] + 0.5*prev = 0.5*40+0.