I need to figure out the deck order and shuffle algorithm that produces the expected output.

Test 1: seed=42, expected first 10 cards: 7H 2S QD 5C AS 9H 3D KH 6S 4C
Test 2: seed=1, expected first 12 cards: 3C JS 7D QH 2D 5S 9C 4H KD 6C AS 8H

Let me implement Fisher-Yates manually with a seeded PRNG. Let me try implementing Fisher-Yates manually with `random.randint` or similar, and try different deck orderings.

Let me try: deck ordered by suits S,H,D,C with ranks A,2,3...K, using Fisher-Yates with `random.randrange` going from n-1 down to 1.

Actually, let me think - I'll need to experiment. Let me try writing it and testing mentally with implementations.

Let me try a manual Fisher-Yates with seed using `random.seed(seed)` and `random.randint(0, i)` for i from len-1 down to 1, with deck order suits=['S','H','D','C'], ranks=['A','2'..'K'].

Since I can't actually test, let me reason: The original code uses `random.shuffle` which is Fisher-Yates internally. The deck order was H,D,C,S with ranks A,2,...,K. The output was wrong.

Let me try implementing Fisher-Yates explicitly going from i=n-1 down to 1, j=randint(0,i), swap. This is what random.shuffle does. So deck order must be different.

Let me try a different deck order. Common orderings:
- Suits in order: Clubs, Diamonds, Hearts, Spades (bridge order)
- Or: Spades, Hearts, Diamonds, Clubs

Let me try suits=['C','D','H','S'], ranks=['A','2','3','4','5','6','7','8','9','10','J','Q','K'].

Without being able to test, I'll have to make educated guesses. Let me try implementing with explicit Fisher-Yates and try variations.

Actually, given the difficulty of guessing the exact algorithm, let me flag this.

{"spec_challenge": "The expected outputs depend on a specific combination of deck ordering (suit/rank order), Fisher-Yates direction (forward vs backward), and PRNG (random.shuffle vs manual randrange/randint calls) that is not specified. Multiple valid Fisher-Yates implementations with a 52-card deck produce different results for the same seed, and the spec does not fix these choices.", "suggested_amendment": "Specify exact deck construction order (e.g., suits in order C,D,H,S; ranks A,2,...,K) and exact Fisher-Yates pseudocode (e.g., 'for i from n-1 down to 1: j = random.randint(0,i); swap deck[i], deck[j]') along with the PRNG to use (e.g., random.seed(seed) then random.randint). Alternatively, provide a reference implementation."}