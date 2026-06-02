Let me trace test 1:
- Alice 1200, Bob 1000
- Alice beats Bob (result=1): expected_Alice = 1/(1+10^((1000-1200)/400)) = 1/(1+10^-0.5) = 1/(1+0.3162) = 0.7597
- Change Alice = 32*(1-0.7597) = 7.69, Alice=1207.69
- Change Bob = 32*(0-0.2403) = -7.69, Bob=992.31

Then Bob beats Alice (result=1 for Bob):
- expected_Bob = 1/(1+10^((1207.69-992.31)/400)) = 1/(1+10^0.5385) = 1/(1+3.456) = 0.2244
- Change Bob = 32*(1-0.2244) = 24.82, Bob=1017.13
- Alice change = 32*(0-0.7756) = -24.82, Alice=1182.87

Result: 1183/1017. But expected: 1206/994.

Expected suggests ratings aren't updated between games — use initial ratings throughout, or batch updates. Let me check: if we use original ratings:
- Game 1: Alice +7.69, Bob -7.69
- Game 2: Bob beats Alice, same expected. Bob change=+7.69, Alice change=-7.69
- Net: Alice=1200, Bob=1000. No.

What if results are accumulated then applied? Same thing.

What about: each game updates using current, but expected 1206/994 means Alice gained 6, Bob lost 6 net. 

Maybe second game's result is interpreted as player1 wins. "Bob Alice 1" means Bob wins. After game 1 (Alice 1207.69, Bob 992.31), Bob beats Alice. Hmm.

Maybe K=16? Game 1: Alice +3.85=1203.85, Bob=996.15. Game 2: expected_Bob=1/(1+10^((1203.85-996.15)/400))=1/(1+10^0.519)=1/(1+3.305)=0.2323. Bob change=16*0.7677=12.28. Bob=1008.43, Alice=1191.57. No.

What if only first game counted? Alice 1208, Bob 992. No, expected 1206/994.

Try: maybe expected uses rating diff of exactly result rounded each time. Game 1: Alice rating 1200 rounded change to int: round(7.69)=8. Alice=1208, Bob=992. Game 2: expected_Bob=1/(1+10^((1208-992)/400))=1/(1+10^0.54)=1/(1+3.467)=0.2239. Change=32*0.7761=24.83→25. Bob=1017, Alice=1183. Still no.

What if result interpretation is different — "Bob Alice 1" means player2 (Alice) wins with result 1? Then second game: Alice wins again. Alice gets +small, Bob -small. After game 1: A=1208, B=992. Game 2 expected_Alice=1/(1+10^((992-1208)/400))=0.7761. Change=32*(1-0.7761)=7.16. Alice=1215, Bob=985. No.

What if K=32 but only applied once total per pair? Net result: Alice won once, Bob won once = draw. expected_Alice in initial state=0.7597. Score=1 (1 win, 1 loss = 1 point each out of 2 games = 0.5 average... or treat as 2 games). 

2 games: Alice scored 1 out of 2 = 0.5 avg, expected per game 0.7597. Change per game = 32*(0.5-0.7597) = -8.31. Total over 2 games = -16.6. Hmm.

Try sum: Alice expected total = 2*0.7597=1.519, actual=1. Change=32*(1-1.519)=-16.6. Alice=1183. No.

What if K=12? 12*(1-1.519)=-6.23. Alice=1194. No.

Expected Alice=1206 means +6. With initial expected 0.7597 over 2 games, actual 1: K*(1-1.519)=K*(-0.519)=+6 → K=-11.56. Negative, doesn't work.

What if expected is calculated wrong direction? Or maybe Alice expected to lose...

Let me try: 32*(1-E)=+6 → E=0.8125. With rating diff d: 1/(1+10^(-d/400))=0.8125 → 10^(-d/400)=0.2308 → -d/400=-0.637 → d=254.7. Not matching 200 diff.

What if only counts wins, ignores draws and the second game already updated? Let me try: after game 1 normally (A=1208,B=992), then for game 2 use SAME expected as game 1 (initial ratings)? expected_Bob_initial=0.2403, change=32*(1-0.2403)=24.31. Bob=992+24=1016, Alice=1208-24=1184. No.

What if rounded BEFORE next calculation? Game1: A=1208, B=992 (rounded). Game2: expected_Bob=1/(1+10^((1208-992)/400))=1/(1+10^0.54). 10^0.54=3.4674. =0.2238. change=32*0.7762=24.84. Round=25. Bob=1017, Alice=1183. No.

Hmm, expected 1206/994. Diff=212. Let me think: maybe wrong direction in formula. expected_a = 1/(1+10^((rating_a-rating_b)/400))? Then for Alice (higher) expected=0.2403 (lower). Game 1: Alice wins (unexpected), gets +32*(1-0.2403)=24.31. Alice=1224, Bob=976. Game 2: now expected_Bob=1/(1+10^((976-1224)/400))=1/(1+10^-0.62)=1/(1+0.2399)=0.8065. Bob wins: change=32*(1-0.8065)=6.19. Bob=982, Alice=1218. No.

Let me try: maybe second result "Bob Alice 1" actually means result for first listed player should be... what gives 1206?

Game 1 normal: A=1207.69, B=992.31.
For final A=1206, need A to lose 1.69 in game 2. Change=-1.69. expected_A=1-(-1.69/32)=1.053. Impossible (>1).

Try K=16: Game 1: A=1203.85, B=996.15. For A=1206, need +2.15 in game 2. expected_A=1-2.15/16=0.866. Diff would need: 10^(-d/400)=0.155 → d=323. But actual d=A-B=207.7. Hmm.

Maybe expected output is wrong but let's check test 2: A=B=1000, draw. Change=32*(0.5-0.5)=0. Output 1000/1000. ✓

For test 1, let me try: maybe the "second" game updates use the ORIGINAL ratings (not updated)?
Game 1: change Alice = 32*(1-0.7597)=7.69
Game 2: change Bob = 32*(1-0.2403)=24.31, change Alice = 32*(0-0.7597)=-24.31

Final Alice = 1200 + 7.69 - 24.31 = 1183.38. No.

What about each player accumulates changes, applied at end:
Alice: +7.69 -24.31 = -16.62. Alice=1183. Same.

What if K-factor different... let me solve directly:
Alice final 1206 = 1200 + delta_A. delta_A=6.
Bob final 994 = 1000 + delta_B. delta_B=-6.

So net Alice gained 6, Bob lost 6. With games where each won once...

If applied with current ratings sequentially:
Game 1: dA1 = K*(1-E1), E1=1/(1+10^-0.5)=0.7597
Game 2: after A=1200+dA1, B=1000-dA1. E_B2=1/(1+10^((1200+dA1-(1000-dA1))/400))=1/(1+10^((200+2dA1)/400))
dB2 = K*(1-E_B2)
dA_total = dA1 - dB2 = 6
dB_total = -dA1 + dB2 = -6 ✓ (consistent)

So dA1 - dB2 = 6. With K=32: dA1=7.69. So dB2=1.69. 
K*(1-E_B2)=1.69 → E_B2=0.947 → 10^((200+2dA1)/400)=0.0559 → (200+15.4)/400=log10(0.0559)=-1.253 → 215.4=-501. Impossible.

So K isn't 32 if sequential. Try K=12:
dA1=12*0.2403=2.884. A=1202.88, B=997.12.
dB2 needed: dA1-dB2=6 → dB2=-3.12. Negative when Bob won = impossible.

Try non-sequential (batch). All updates use original ratings:
dA1=K*0.2403, dB1=-K*0.2403
dA2=K*(0-0.7597)=-K*0.7597, dB2=K*(1-0.2403)=K*0.7597
Net dA=K*(0.2403-0.7597)=-K*0.5194
For dA=6: K=-11.55. Impossible.

What if "result" column is for player2 not player1?
Test 1: "Alice Bob 1" → Bob wins? 
Game 1: Bob wins. dA1=32*(0-0.7597)=-24.31. A=1175.69, B=1024.31.
Game 2: "Bob Alice 1" → Alice wins. E_A2=1/(1+10^((1024.31-1175.69)/400))=1/(1+10^-0.378)=1/(1+0.4185)=0.7050. dA2=32*(1-0.7050)=9.44. A=1185.13, B=1014.87. No.

Hmm. What if result is from player1's perspective but they're switched in second? Unclear...

Let me try yet another interpretation: the result column means "1=player1 wins, 0=player2 wins, 0.5=draw" (standard), but games processed both ways with K halved... no.

Let me look at this differently. 1206 and 994. Average=1100? No, (1206+994)/2=1100. Original avg=1100. ✓ (Elo preserves sum).

Game 1 (Alice wins): A=1207.69, B=992.31, K=32 standard.
Game 2 (Bob wins): need A=1206, so A lost 1.69 in game 2. K*(0-E_A2)=-1.69 → E_A2=0.0528. So Bob's rating much higher than Alice's now? E_A2=0.0528 means rating diff B-A = 400*log10((1/E)-1)=400*log10(17.94)=400*1.254=501.6. But B-A actual=-215.4. Impossible.

What if K=32 in game 1 but Alice gets +6 directly (rounded), then game 2 cancels out... unlikely.

Let me try: maybe it's expected 1208 not 1206. Or maybe ratings rounded each step:
Game 1: A=1208, B=992. Game 2: E_B=1/(1+10^(216/400))=1/(1+10^0.54)=0.2237. dB=32*0.7763=24.84. Round=25. So B=992+25=1017, A=1208-25=1183. Not 1206.

What if K used differently per game / scaled? K=8?
Game 1: dA=8*0.2403=1.92. A=1201.92, B=998.08.
Game 2: E_B=1/(1+10^(3.84/400))=1/(1+10^0.0096)=1/(1+1.0224)=0.4945. dB=8*0.5055=4.04. A=1197.87, B=1002.12. No.

K varies? Let me solve for the relationship.
Let x = dA1, y = dB2 (both positive Elo changes for winners).
A_final = 1200 + x - y = 1206 → x-y=6
B_final = 1000 - x + y = 994 → -x+y=-6 ✓

So x-y=6. x=K1*(1-1/(1+10^-0.5))=K1*0.2403