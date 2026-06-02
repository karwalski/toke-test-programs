import sys
from collections import defaultdict

def solve():
    words = []
    for line in sys.stdin:
        word = line.strip()
        if word:
            words.append(word)
    
    # Group words by their sorted characters (anagram signature)
    anagram_groups = defaultdict(list)
    for word in words:
        signature = ''.join(sorted(word.lower()))
        anagram_groups[signature].append(word)
    
    # Find the longest anagram chain
    longest_chain = []
    for group in anagram_groups.values():
        if len(group) > len(longest_chain):
            longest_chain = group
    
    # Output the longest chain
    if longest_chain:
        print(' '.join(longest_chain))

solve()