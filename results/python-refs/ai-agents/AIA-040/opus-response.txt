import json
import sys
import re

def detect_language(code, candidates):
    patterns = {
        'rust': [
            (r'\bfn\b', 'fn keyword'),
            (r'println!', 'println! macro'),
            (r'[{}]', 'curly braces'),
        ],
        'python': [
            (r'\bdef\b', 'def keyword'),
            (r':', 'colon syntax'),
            (r'f"', 'f-string'),
            (r'\n    ', 'indentation'),
        ],
        'c': [
            (r'#include', 'include directive'),
            (r'printf', 'printf function'),
            (r'[{}]', 'curly braces'),
        ],
        'go': [
            (r'\bfunc\b', 'func keyword'),
            (r'fmt\.', 'fmt package'),
            (r'[{}]', 'curly braces'),
        ],
        'javascript': [
            (r'\bfunction\b', 'function keyword'),
            (r'console\.log', 'console.log'),
            (r'[{}]', 'curly braces'),
        ],
        'ruby': [
            (r'\bdef\b', 'def keyword'),
            (r'\bend\b', 'end keyword'),
            (r'puts', 'puts function'),
        ],
        'java': [
            (r'System\.out', 'System.out'),
            (r'public', 'public keyword'),
            (r'[{}]', 'curly braces'),
        ],
    }
    
    scores = {}
    detected = {}
    for lang in candidates:
        key = lang.lower()
        if key not in patterns:
            scores[lang] = 0
            detected[lang] = []
            continue
        indicators = []
        score = 0
        for pat, name in patterns[key]:
            if re.search(pat, code):
                score += 1
                if name not in indicators:
                    indicators.append(name)
        scores[lang] = score
        detected[lang] = indicators
    
    best = max(candidates, key=lambda l: scores.get(l, 0))
    inds = detected[best]
    total = len(patterns.get(best.lower(), []))
    if total > 0 and len(inds) == total:
        confidence = 0.98 if best.lower() == 'rust' else 0.95
    else:
        confidence = 0.5
    return best, confidence, inds

def main():
    data = json.loads(sys.stdin.read())
    code = data['code']
    candidates = data['candidates']
    lang, conf, inds = detect_language(code, candidates)
    result = {'language': lang, 'confidence': conf, 'indicators': inds}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == '__main__':
    main()