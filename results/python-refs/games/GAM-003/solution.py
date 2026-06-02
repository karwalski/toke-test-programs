import random
import sys
from collections import deque

def main():
    data = sys.stdin.read().strip().split()
    seed = int(data[0])
    random.seed(seed)
    # Build deck: suits S,H,D,C and ranks 2..A (values 2..14)
    suits = ['S','H','D','C']
    deck = [(r, s) for s in suits for r in range(2, 15)]
    random.shuffle(deck)
    # Deal first 26 to P1, next 26 to P2
    p1 = deque(deck[:26])
    p2 = deque(deck[26:])
    rounds = 0
    max_rounds = 100000
    winner = None
    while p1 and p2 and rounds < max_rounds:
        rounds += 1
        c1 = p1.popleft()
        c2 = p2.popleft()
        pile = [c1, c2]
        while c1[0] == c2[0]:
            # War: each places up to 3 face-down then 1 face-up
            # If insufficient cards, player loses
            if len(p1) < 4:
                # P1 cannot war -> P2 wins all
                # Move remaining of p1 and pile to p2
                while p1:
                    pile.append(p1.popleft())
                for card in pile:
                    p2.append(card)
                break
            if len(p2) < 4:
                while p2:
                    pile.append(p2.popleft())
                for card in pile:
                    p1.append(card)
                break
            for _ in range(3):
                pile.append(p1.popleft())
                pile.append(p2.popleft())
            c1 = p1.popleft()
            c2 = p2.popleft()
            pile.append(c1)
            pile.append(c2)
        else:
            # no break: normal compare
            if c1[0] > c2[0]:
                for card in pile:
                    p1.append(card)
            else:
                for card in pile:
                    p2.append(card)
            continue
        # if we broke out due to insufficient cards, loop will exit
    if not p1:
        winner = 2
    elif not p2:
        winner = 1
    else:
        # Stalemate; declare by card count
        winner = 1 if len(p1) > len(p2) else 2
    print(f"Player {winner} wins after {rounds} rounds")

main()
