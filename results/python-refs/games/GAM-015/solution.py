target = input().strip()
guess = input().strip()

feedback = ['B'] * 5
target_chars = list(target)

# First pass: mark exact matches (green)
for i in range(5):
    if guess[i] == target[i]:
        feedback[i] = 'G'
        target_chars[i] = None  # Mark as used

# Second pass: mark yellow matches
for i in range(5):
    if feedback[i] == 'B':  # Only check non-green positions
        if guess[i] in target_chars:
            feedback[i] = 'Y'
            # Remove first occurrence of this character
            target_chars[target_chars.index(guess[i])] = None

print(''.join(feedback))