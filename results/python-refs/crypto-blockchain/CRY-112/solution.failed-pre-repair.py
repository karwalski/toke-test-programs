import math
import re
from collections import Counter

def calculate_entropy(password):
    if not password:
        return 0
    
    # Count frequency of each character
    char_counts = Counter(password)
    length = len(password)
    
    # Calculate Shannon entropy
    entropy = 0
    for count in char_counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    
    return entropy

def score_password(password):
    if not password:
        return 0
    
    score = 0
    
    # Length scoring (0-25 points)
    length = len(password)
    if length >= 12:
        score += 25
    elif length >= 8:
        score += 20
    elif length >= 6:
        score += 15
    elif length >= 4:
        score += 10
    else:
        score += 5
    
    # Character class scoring (0-25 points)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[^a-zA-Z0-9]', password))
    
    char_classes = sum([has_lower, has_upper, has_digit, has_special])
    score += char_classes * 6  # Up to 24 points for 4 classes
    if char_classes == 4:
        score += 1  # Bonus point for all classes
    
    # Entropy scoring (0-25 points)
    entropy = calculate_entropy(password)
    entropy_score = min(25, int(entropy * 5))  # Scale entropy to 0-25
    score += entropy_score
    
    # Pattern penalties (0-25 points, but subtract from total)
    penalties = 0
    
    # Common passwords
    common_passwords = [
        'password', '123456', '123456789', 'qwerty', 'abc123', 
        'password123', 'admin', 'letmein', 'welcome', 'monkey',
        '1234567890', 'football', 'iloveyou', 'admin123', 'welcome123'
    ]
    
    if password.lower() in common_passwords:
        penalties += 20
    
    # Sequential characters (like 123, abc)
    sequential_count = 0
    for i in range(len(password) - 2):
        if (ord(password[i+1]) == ord(password[i]) + 1 and 
            ord(password[i+2]) == ord(password[i]) + 2):
            sequential_count += 1
    
    penalties += min(15, sequential_count * 5)
    
    # Repeated characters
    repeat_penalty = 0
    char_counts = Counter(password)
    for count in char_counts.values():
        if count > 1:
            repeat_penalty += (count - 1) * 2
    
    penalties += min(10, repeat_penalty)
    
    # Apply penalties
    score -= penalties
    
    # Ensure score is between 0 and 100
    score = max(0, min(100, score))
    
    return score

def get_strength(score):
    if score >= 90:
        return "VERY_STRONG"
    elif score >= 70:
        return "STRONG"
    elif score >= 50:
        return "GOOD"
    elif score >= 30:
        return "FAIR"
    else:
        return "WEAK"

# Read password from stdin
password = input().strip()

# Calculate score and strength
score = score_password(password)
strength = get_strength(score)

# Output results
print(score)
print(strength)