import json
import sys
import math
import re

def calculate_entropy(password):
    """Calculate password entropy in bits"""
    if not password:
        return 0
    
    # Count character set size
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'[0-9]', password):
        charset_size += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        charset_size += 32  # Common symbols
    
    if charset_size == 0:
        return 0
    
    return len(password) * math.log2(charset_size)

def check_common_patterns(password):
    """Check for common password patterns"""
    patterns = []
    
    # Sequential characters
    if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
        patterns.append("sequential_letters")
    
    if re.search(r'(012|123|234|345|456|567|678|789)', password):
        patterns.append("sequential_numbers")
    
    # Repeated characters
    if re.search(r'(.)\1{2,}', password):
        patterns.append("repeated_characters")
    
    # Keyboard patterns
    keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '1234', 'qazwsx']
    for pattern in keyboard_patterns:
        if pattern in password.lower():
            patterns.append("keyboard_pattern")
            break
    
    return patterns

def check_dictionary_words(password):
    """Check for common dictionary words"""
    # Common weak passwords and dictionary words
    common_words = [
        'password', 'admin', 'user', 'login', 'welcome', 'hello', 'world',
        'test', 'guest', 'master', 'secret', 'access', 'computer', 'system',
        'root', 'default', 'service', 'pass', 'word', 'love', 'god', 'sex',
        'money', 'live', 'home', 'work', 'school', 'company', 'name'
    ]
    
    found_words = []
    password_lower = password.lower()
    
    for word in common_words:
        if word in password_lower:
            found_words.append(word)
    
    return found_words

def analyze_password(password):
    """Analyze password strength and return detailed results"""
    issues = []
    suggestions = []
    score = 0
    
    # Length analysis
    length = len(password)
    if length < 8:
        issues.append("too_short")
        suggestions.append("Use at least 8 characters")
    elif length >= 8:
        score += 20
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10
    
    # Character diversity
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_symbol = bool(re.search(r'[^a-zA-Z0-9]', password))
    
    char_types = sum([has_lower, has_upper, has_digit, has_symbol])
    
    if not has_lower:
        issues.append("no_lowercase")
        suggestions.append("Add lowercase letters")
    
    if not has_upper:
        issues.append("no_uppercase")
        suggestions.append("Add uppercase letters")
    
    if not has_digit:
        issues.append("no_numbers")
        suggestions.append("Add numbers")
    
    if not has_symbol:
        issues.append("no_symbols")
        suggestions.append("Add special characters")
    
    # Score based on character diversity
    score += char_types * 10
    
    # Check for common patterns
    patterns = check_common_patterns(password)
    if patterns:
        issues.extend(patterns)
        suggestions.append("Avoid common patterns")
        score -= len(patterns) * 10
    
    # Check for dictionary words
    dict_words = check_dictionary_words(password)
    if dict_words:
        issues.append("dictionary_words")
        suggestions.append("Avoid common words")
        score -= len(dict_words) * 15
    
    # Calculate entropy
    entropy = calculate_entropy(password)
    
    # Adjust score based on entropy
    if entropy < 30:
        score -= 20
    elif entropy >= 50:
        score += 20
    
    # Ensure score is within bounds
    score = max(0, min(100, score))
    
    # Determine strength level
    if score < 30:
        strength = "weak"
    elif score < 50:
        strength = "fair"
    elif score < 80:
        strength = "strong"
    else:
        strength = "very_strong"
    
    return {
        "score": score,
        "strength": strength,
        "entropy_bits": round(entropy, 1),
        "issues": issues,
        "suggestions": suggestions
    }

def main():
    password = input().strip()
    result = analyze_password(password)
    print(json.dumps(result))

if __name__ == "__main__":
    main()