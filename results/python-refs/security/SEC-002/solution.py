import json
import sys
import math
import re

def calculate_entropy(password):
    if not password:
        return 0
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'[0-9]', password):
        charset_size += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        charset_size += 32
    if charset_size == 0:
        return 0
    return len(password) * math.log2(charset_size)

def analyze_password(password):
    issues = []
    suggestions = []
    score = 0
    length = len(password)
    
    if length < 8:
        issues.append("too_short")
        suggestions.append("Use at least 8 characters")
    if length >= 8:
        score += 20
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10
    
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_symbol = bool(re.search(r'[^a-zA-Z0-9]', password))
    char_types = sum([has_lower, has_upper, has_digit, has_symbol])
    
    if not has_lower:
        issues.append("no_lowercase"); suggestions.append("Add lowercase letters")
    if not has_upper:
        issues.append("no_uppercase"); suggestions.append("Add uppercase letters")
    if not has_digit:
        issues.append("no_numbers"); suggestions.append("Add numbers")
    if not has_symbol:
        issues.append("no_symbols"); suggestions.append("Add special characters")
    
    score += char_types * 10
    
    patterns = []
    if re.search(r'(012|123|234|345|456|567|678|789)', password):
        patterns.append("sequential_numbers")
    if re.search(r'(.)\1{2,}', password):
        patterns.append("repeated_characters")
    keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '1234', 'qazwsx']
    for p in keyboard_patterns:
        if p in password.lower():
            patterns.append("keyboard_pattern")
            break
    if patterns:
        issues.extend(patterns)
        suggestions.append("Avoid common patterns")
        score -= len(patterns) * 10
    
    common_words = ['password','admin','user','login','welcome','hello','world',
                    'test','guest','master','secret','access','computer','system',
                    'root','default','service','love','money']
    dict_words = [w for w in common_words if w in password.lower()]
    if dict_words:
        issues.append("dictionary_words")
        suggestions.append("Avoid common words")
        score -= len(dict_words) * 15
    
    entropy = calculate_entropy(password)
    
    common_passwords = {'password','password123','123456','12345678','qwerty','abc123',
                        'monkey','letmein','dragon','111111','baseball','iloveyou',
                        'trustno1','sunshine','master','welcome','shadow','ashley',
                        'football','jesus','michael','ninja','mustang','password1'}
    if password.lower() in common_passwords:
        issues.append("common_password")
        score -= 50
    
    if entropy < 30:
        score -= 20
    elif entropy >= 60:
        score += 20
    
    score = max(0, min(100, score))
    
    if score < 40:
        strength = "weak"
    elif score < 60:
        strength = "fair"
    elif score < 85:
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
    password = input()
    result = analyze_password(password)
    print(result["strength"])

if __name__ == "__main__":
    main()