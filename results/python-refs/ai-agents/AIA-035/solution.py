import sys
import json
import re
from collections import Counter

def detect_language(text):
    # Simple language detection based on character patterns and common words
    text = text.lower().strip()
    
    # Language patterns and indicators
    language_indicators = {
        'en': {
            'words': ['the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'with', 'for', 'as', 'was', 'on', 'are', 'you', 'this', 'be', 'at', 'have'],
            'patterns': [r'\bthe\b', r'\band\b', r'\byou\b', r'\bis\b', r'\bwith\b']
        },
        'fr': {
            'words': ['le', 'de', 'et', 'un', 'il', 'être', 'et', 'en', 'avoir', 'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne', 'se', 'pas', 'tout', 'plus', 'par', 'grand', 'il', 'me', 'même', 'tout', 'si', 'nous', 'comme', 'mais', 'ou', 'très', 'mon', 'votre', 'vous', 'comment', 'bonjour', 'monde', 'aujourd', 'allez'],
            'patterns': [r'\ble\b', r'\bde\b', r'\bet\b', r'\bun\b', r'\bvous\b', r'\bcomment\b', r'\bbonjour\b', r'\bmonde\b', r'\ballez\b']
        },
        'es': {
            'words': ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'una', 'pero', 'todo', 'bien', 'más', 'muy', 'hola', 'como'],
            'patterns': [r'\bel\b', r'\bla\b', r'\bque\b', r'\bhola\b', r'\bcomo\b']
        },
        'de': {
            'words': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich', 'des', 'auf', 'für', 'ist', 'im', 'dem', 'nicht', 'ein', 'eine', 'als', 'auch', 'es', 'an', 'werden', 'aus', 'er', 'hat', 'dass', 'sie', 'nach', 'wird', 'bei', 'einer', 'um', 'am', 'sind', 'noch', 'wie', 'einem', 'über', 'einen', 'so', 'zum', 'war', 'haben', 'nur', 'oder', 'aber', 'vor', 'zur', 'bis', 'mehr', 'durch', 'man', 'sein', 'wurde', 'sei', 'in'],
            'patterns': [r'\bder\b', r'\bdie\b', r'\bund\b', r'\bdas\b', r'\bist\b']
        }
    }
    
    # Calculate scores for each language
    language_scores = {}
    
    for lang, indicators in language_indicators.items():
        score = 0
        total_checks = 0
        
        # Check for word matches
        words = re.findall(r'\b\w+\b', text)
        word_matches = sum(1 for word in words if word in indicators['words'])
        total_checks += len(words)
        score += word_matches * 2
        
        # Check for pattern matches
        for pattern in indicators['patterns']:
            matches = len(re.findall(pattern, text))
            score += matches * 3
            total_checks += 1
        
        if total_checks > 0:
            language_scores[lang] = score / total_checks
        else:
            language_scores[lang] = 0
    
    # Determine primary language
    if not language_scores or max(language_scores.values()) == 0:
        primary = 'en'
        confidence = 0.5
    else:
        primary = max(language_scores, key=language_scores.get)
        max_score = language_scores[primary]
        confidence = min(max_score, 1.0)
        
        # Boost confidence for clear matches
        if max_score > 0.3:
            confidence = min(0.98, confidence + 0.5)
    
    # Determine secondary languages
    secondary = []
    threshold = 0.2
    for lang, score in language_scores.items():
        if lang != primary and score > threshold and score > max(language_scores.values()) * 0.3:
            secondary.append(lang)
    
    return primary, confidence, secondary

# Read input from stdin
text = sys.stdin.read().strip()

# Detect language
primary, confidence, secondary = detect_language(text)

# Format output
result = {
    "primary": primary,
    "confidence": confidence,
    "secondary": secondary
}

# Output JSON without spaces after separators to match expected format
print(json.dumps(result, separators=(',', ':')))