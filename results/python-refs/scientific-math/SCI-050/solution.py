Looking at test 1: expected hull is `(0,0) (1,1) (4,4) (0,3)`. The point (1,1) is on the segment from (0,0) to (4,4) — it's collinear and should be considered interior. But the expected output includes it. And (2,2) is also collinear but excluded.

Wait, expected includes (1,1) but excludes (2,2). Both are on line from (0,0) to (4,4). That's strange. Unless... the hull includes (1,1) as a "vertex" but not (2,2). This contradicts the spec saying "exclude interior" / collinear handling.

Hmm, but expected area is `X.XXXXXX` (literal placeholder), suggesting test 1 may not strictly check the area. Let me match the exact expected output for test 1.

Hull `(0,0) (1,1) (4,4) (0,3)` — perhaps the rule is to keep collinear points except those strictly between, but (1,1) and (2,2) are both strictly between (0,0) and (4,4)...

Wait, maybe the expected output is just wrong/weird and we need to match it. Looking again — maybe the algorithm keeps collinear points on the hull edge but the current code keeps both (1,1) and (2,2). Expected keeps only (1,1). 

Actually the `<` vs `<=` in cross product: with `<=`, we remove collinear points (strictly convex hull). Current uses `<` which keeps all collinear. Expected has (1,1) but not (2,2)...

Maybe expected sorts differently. With current sort by (angle, dist), among collinear points sorted by distance ascending: (1,1), (2,2), (4,4). With `<=` we'd remove (1,1) and (2,2), keeping only (4,4). That gives `(0,0) (4,4) (0,3)`.

The expected `(0,0) (1,1) (4,4) (0,3)` is genuinely odd. Test 1 area is `X.XXXXXX` — literally that string? That would mean any area passes if we print "X.XXXXXX". 

I think the test 1 expected is a malformed spec. Let me challenge.

{"spec_challenge": "Test case 1 expected output contains a literal placeholder 'X.XXXXXX' for the area instead of a numeric value, and the hull points '(0,0) (1,1) (4,4) (0,3)' inconsistently include the collinear interior point (1,1) on segment (0,0)-(4,4) while excluding the other collinear point (2,2). No deterministic convex-hull algorithm produces this output: a strict hull excludes both (1,1) and (2,2), while a permissive hull includes both. The expected output is internally inconsistent and cannot be matched.", "suggested_amendment": "Fix test 1 expected output to a deterministic convex hull. For strict hull (excluding collinear interior): 'Hull points: (0,0) (4,4) (0,3)\\nHull area: 6.000000'. Also replace the 'X.XXXXXX' placeholder with the actual numeric area value."}