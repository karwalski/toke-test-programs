Let me analyze the expected outputs to reverse-engineer the scoring.

Test 2: n1, score 95. capacity_pct=10, latency=5ms.
Test 1: r1 score 85 (cap 30, lat 50), r2 score 70 (cap 80, lat 30), r3 score 45 (cap 90, lat 10).

Capacity score seems inverted: lower capacity_pct (more available) = better. Available capacity = 100 - capacity_pct.
- r1: avail=70, r2: avail=20, r3: avail=10
- n1: avail=90

Latency score: 100 - latency_ms (capped)
- r1: 50, r2: 70, r3: 90
- n1: 95

Test 2 single node, proximity is perfect = 100.
Score = 0.4*100 + 0.3*95 + 0.3*90 = 40+28.5+27 = 95.5 → 95 ✓ (or rounds to 96?). Let me check: round(95.5) in Python uses banker's rounding → 96. Hmm.

Try latency_score = 100 - latency: n1=95, capacity_score=100-cap=90, proximity=100.
0.4*100+0.3*95+0.3*90 = 40+28.5+27 = 95.5. Python round → 96. But expected 95.

Maybe int truncation: int(95.5)=95 ✓.

Test 1:
Direct NY→London ≈ 5570 km.
- r1 (45,-40): NY→r1 ≈ 3300, r1→London ≈ 3700, total ≈ 7000. extra/direct ≈ 0.257, prox=74.3
- r2 (48.8, 2.3): NY→r2 ≈ 5837, r2→London ≈ 343, total ≈ 6180. extra ≈ 0.109, prox=89.1
- r3 (40,-75): NY→r3 ≈ 130, r3→London ≈ 5680, total≈5810. extra≈0.043, prox=95.7

Scores:
- r1: 0.4*74.3 + 0.3*50 + 0.3*70 = 29.72+15+21 = 65.72 → not 85
- r2: 0.4*89.1 + 0.3*70 + 0.3*20 = 35.64+21+6 = 62.64 → not 70
- r3: 0.4*95.7 + 0.3*90 + 0.3*10 = 38.28+27+3 = 68.28 → not 45

Hmm. Let me try: maybe proximity = how intermediate (closer to midpoint).

Midpoint NY-London ≈ (46.1, -37.05). 
- r1 (45,-40): distance to midpoint small → high prox
- r2 (48.8, 2.3): far from midpoint
- r3 (40,-75): far from midpoint

r1 should score highest in proximity. Maybe simple ordering based on this.

Let me try: scores 85, 70, 45 differ by 15 and 25. Or maybe simpler heuristic.

Try: score = 100 - latency_ms - some_capacity_penalty?
- r1: 100-50+(something with cap 30) = 50 + 35 = 85? if cap_bonus = (100-cap)/2 = 35. ✓
- r2: 100-30 - ... = 70. cap_bonus=(100-80)/2=10. 70+10=80, not 70.

Try score = (100-latency)*0.5 + (100-cap)*0.5 + proximity_bonus:
- r1: 25+35=60+25=85
- r2: 35+10=45+25=70  
- r3: 45+5=50-5=45?

Maybe score doesn't follow exact formula. Let me try: nodes sorted by proximity to midpoint, then score = 100 - some penalty.

r1 is closest to midpoint, r2 next, r3 last. Composite likely matches expected. Let me try a different formula.

Try: proximity_score weight differently. Let prox compute distance to midpoint and normalize.

Actually let me just check: maybe latency_score uses /100 not /200:
- r1: lat=50, score=50. r2: lat=70. r3: lat=90.
Same as before mostly.

Let me try with proximity = 100 - (dist_to_midpoint / direct_dist)*100:
midpoint ≈ (46.1, -37.05), direct ≈ 5570.
- r1: dist to mid ≈ small (45,-40 vs 46.1,-37.05) ≈ √(1.1² + 2.95²)*111 ≈ 350km. prox = 100-350/5570*100 = 93.7
- r2: dist to mid: (48.8-46.1, 2.3-(-37.05))=(2.7, 39.35). ~ huge. Use haversine. ≈ 2900km. prox=100-52=48
- r3: dist (40-46.1, -75-(-37.05))=(-6.1, -37.95). ≈ 3000km. prox=46

Scores:
- r1: 0.4*93.7+0.3*50+0.3*70 = 37.48+15+21=73.48 → not 85
- r2: 0.4*48+0.3*70+0.3*20=19.2+21+6=46.2 → not 70
- r3: 0.4*46+0.3*90+0.3*10=18.4+27+3=48.4 → ~45 ✓

Hmm r3 matches. Let me try weights differently.

Score r1=85 with cap 30 lat 50. If score = (100-cap)*0.5 + (100-lat)*0.3 + prox*0.2:
- r1: 35+15+prox*0.2=50+prox*0.2. need 85 → prox=175. No.

Try: score = (100-cap) + something:
- r1: 70+15=85. So 70 + (100-lat)*0.3 = 70+15=85 ✓
- r2: 20+(100-30)*?=20+50? No, 20+70*?... need 70. 20+50=70 if just add (100-lat). r2: 20+70=90, no.

r1: 70+15=85 where 15=(100-50)*0.3
r2: 20+...=70. need 50. (100-30)=70, *5/7? 
r3: 10+...=45. need 35. (100-10)=90.

r1: 70+15=85
r2: 20+(70-something). Hmm.

Try score = (100-cap)+(100-lat)/2 - penalty:
- r1: 70+25=95. need 85, penalty 10
- r2: 20+35=55. need 70, bonus 15
- r3: 10+45=55. need 45, penalty 10

Doesn't match a pattern.

Let me try: (100-cap)*0.4 + (100-lat)*0.3 + prox*0.3:
- r1: 28+15+prox*0.3=43+prox*0.3=85 → prox=140. No.

Try weights 0.3, 0.3, 0.4 on (proximity, latency_inv, capacity_inv):
n1: 0.3*100+0.3*95+0.4*90 = 30+28.5+36=94.5→94 (close to 95)
r1: prox*0.3+15+0.4*70=prox*0.3+43=85→prox=140. No.

Try: capacity weight 0.3 with raw capacity_pct inverted to (100-cap):
What if proximity is just a bonus rank-based?

Let me try: score = (proximity_rank_score)*0.4 + (100-lat)*0.3 + (100-cap)*0.3 where proximity_rank gives 100/66/33 or similar:

For test 1, sorting by closeness to midpoint: r1=1st(100), r2=2nd, r3=3rd.
- r1: 100*0.4+50*0.3+70*0.3 = 40+15+21=76. Not 85.

Let me try: 100*0.5+50*0.3+70*0.3 = 50+15+21=86. Close to 85!
- r2: rank 2 → 50? 50*0.5+70*0.3+20*0.3=25+21+6=52. Not 70.

Hmm. Let me look for simpler patterns. 

r1=85, r2=70, r3=45. Differences 15, 25. 
n1=95.

What if score = 100 - latency_ms*0.3 - capacity_pct*0.3 - distance_penalty*0.4?

n1: 100 - 1.5 - 3 - prox_penalty*0.4 = 95.5 - prox_pen*0.4 = 95 → prox_pen ≈ 1.25. Roughly 0 → score=95.5→95 (int trunc). ✓

r1: 100 - 15 - 9 - prox*0.4 = 76 - prox*0.4 = 85? Negative penalty. So prox could be a bonus.

Let me reconsider: maybe proximity to PATH (line between sender and recipient) not midpoint.

Cross-track distance from r1(45,-40) to NY-London great circle: r1 is roughly ON the great circle path. So small.
r3(40,-75) is near sender — also ON path (sender end).
r2(48.8, 2.3) is near recipient (London) — ON path too.

All three are near the great circle. So proximity-to-path doesn't differentiate well. Maybe "geographically intermediate" — preferring middle of path.

Position along path (0=sender, 1=recipient):
- r1: ~middle, ~0.5
- r2: ~recipient, ~0.95
- r3: ~sender, ~0.05

Score for being intermediate: peak at 0.5. Could be 100*(1 - |pos-0.5|*2):
- r1: 100*1=100
- r2: 100*(1-0.9)=10
- r3: 100*(1-0.9)=10

Composite (weights 0.4, 0.3, 0.3 with inverted lat and cap):
- r1: 0.4*100 + 0.3*50 + 0.3*70 = 40+15+21 = 76. Not 85.

Try: 0.5, 0.25, 0.25:
- r1: 50+12.5+17.5=80. No.

0.4*prox + 0.3*(100-lat) + 0.3*(100-cap):
- r1: 40+15+21=76
- r2: 4+21+6=31, but expected 70
- r3: 4+27+3=34, but expected 45

That's wrong since r2 has high score.

Maybe proximity isn't path-position; perhaps lower is better for cap and lat both, and proximity is just minor.

Looking at r1=85: cap=30, lat=50 → low cap+low lat ≈ good
r2=70: cap=80, lat=30 → high cap penalty
r3=45: cap=90, lat=10 → very high cap

So capacity dominates. Score ≈ 100 - capacity_pct + something:
- r1: 100-30=70 +15=85
- r2: 100-80=20 +50=70  
- r3: 100-90=10 +35=45
- n1: 100-10=90 +5=95

Bonus: r1=15, r2=50, r3=35, n1=5.

For r1: latency=50, bonus=15? Hmm. 
For r2: lat=30, bonus=50? 
For r3: lat=10, bonus=35?
For n1: lat=5, bonus=5?

Not directly latency.

What if bonus relates to latency in some way + proximity?

n1: proximity=100% (on direct line), latency=5. bonus=5.
r1: bonus=15
r2: bonus=50  
r3: bonus=35

Hmm n1 bonus 5 = latency. r3 bonus 35? lat=10... 35=?

What if: score = (100-cap)*0.7 + (100-lat)*0.3:
- r1: 49+15=64. No.

score = (100-cap) + (100-lat)*0.3:
- r1: 70+15=85 ✓
- r2: 20+21=41. expected 70 ✗

Hmm. Try (100-cap)*0.5 + (100-lat)*0.5 + prox bonus:
- r1: 35+25=60, need 25 more
- r2: 10+35=45, need 25 more  
- r3: 5+45=50