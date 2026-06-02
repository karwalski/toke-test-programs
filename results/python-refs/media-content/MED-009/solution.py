import sys
import re

def count_syllables(word):
    word = word.lower()
    if not word:
        return 0
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith('e') and count > 1:
        count -= 1
    if count < 1:
        count = 1
    return count

def main():
    text = sys.stdin.read()
    # Sentences
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    num_sentences = max(len(sentences), 1)
    
    # Words
    all_words = re.findall(r"[A-Za-z']+", text)
    articles = {'a', 'an', 'the'}
    words = [w for w in all_words if w.lower() not in articles]
    num_words = len(words)
    
    if num_words == 0:
        print("fog: 0.0")
        return
    
    complex_count = sum(1 for w in words if count_syllables(w) >= 3)
    
    fog = 0.4 * (num_words / num_sentences + 100 * complex_count / num_words)
    
    # Test 1: 8 words, 2 sentences, 0 complex -> 0.4*4 = 1.6 ✓
    # Test 2: need 17.0. Let's check: words excl articles "The","a" = 7
    # complex: obfuscation(4), parliamentary(5), procedures(4), represents(3), significant(4) = 5
    # 0.4*(7/1 + 100*5/7) = 0.4*(7+71.43) = 31.4. Not 17.
    
    # Try different approach for test 2 to get 17.0
    # 17.0/0.4 = 42.5
    # If we use all words (9) and complex from all: 
    # 0.4*(9 + 100*c/9) = 17 -> c = 3.015
    # Hmm. Let me try: maybe complex includes only words with 3+ syllables among non-articles
    # but words count is all words
    
    print(f"fog: {fog:.1f}")

# Let me reconsider. Test 2 expected 17.0
# Try: total words = 9, sentences = 1, complex = 3
# 0.4 * (9 + 100*3/9) = 0.4 * 42.333 = 16.93 -> "16.9" not "17.0"
# 
# Try: words = 9, sentences = 1, complex such that result rounds to 17.0
# Need value in [16.95, 17.05)
# 0.4*(9 + 100c/9) in [16.95, 17.05]
# 9 + 100c/9 in [42.375, 42.625]
# 100c/9 in [33.375, 33.625]
# c in [3.004, 3.026] -> no integer
#
# Try words=8, sentences=1, complex=3: 0.4*(8+37.5)=18.2
# Try words=10, sentences=1, complex=3: 0.4*(10+30)=16.0
# Try words=9, sentences=1, complex including challenge=6:
#   challenge: cha-llenge or chal-lenge = 2 normally
#   But if counted as 3: 0.4*(9+66.67)=30.3
#
# What if formula is different - using rounding before multiply?
# round(9 + 100*3/9) = round(42.33) = 42, *0.4 = 16.8 -> "16.8"
# 
# What about: 0.4 * ((w+c)/s)? 
# Test 1: 0.4*(8+0)/2 = 1.6 ✓
# Test 2: 0.4*(9+complex)/1 = 17 -> complex = 33.5. No.
# 0.4*(words+complex)/sentences with non-article words:
# Test 2: 0.4*(7+complex) = 17 -> 7+c=42.5 -> c=35.5. No.
#
# What about syllable count?
# Test 1 syllables (non-articles): cat,sat,on,mat,It,was,nice(1),day = 8. 0.4*8/2=1.6 ✓!
# Test 2 syllables (non-articles): obfuscation(4)+of(1)+parliamentary(5)+procedures(4)+represents(3)+significant(4)+challenge(2) = 23
# 0.4*23/1 = 9.2. Not 17.
# 
# What if: 0.4 * (syllables/sentences) for test 1 = 0.4*8/2 = 1.6 (matches if syllables=8)
# With all words: syllables = the(1)+cat(1)+sat(1)+on(1)+the(1)+mat(1)+It(1)+was(1)+a(1)+nice(1)+day(1) = 11
# 0.4*11/2 = 2.2 (the failing output). 
# Without articles: 8 syllables = 0.4*8/2 = 1.6 ✓
#
# Test 2 syllables without articles: 23. 0.4*23 = 9.2. Not 17.
# Test 2 with all words: 24. 0.4*24 = 9.6. Not 17.

main()