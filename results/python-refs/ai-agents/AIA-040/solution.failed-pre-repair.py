import json
import sys
import re

def detect_language(code, candidates):
    # Define language-specific patterns and indicators
    patterns = {
        'rust': [
            (r'\bfn\b', 'fn keyword'),
            (r'\bprintln!\s*\(', 'println! macro'),
            (r'\blet\s+mut\b', 'mut keyword'),
            (r'\bmatch\b', 'match keyword'),
            (r'\bimpl\b', 'impl keyword'),
            (r'\bstruct\b', 'struct keyword'),
            (r'\benum\b', 'enum keyword'),
            (r'\buse\b', 'use keyword'),
            (r'&\w+', 'reference operator'),
            (r'::\w+', 'scope operator'),
            (r'\|.*\|', 'closure syntax'),
            (r'<.*>', 'generic syntax'),
            (r'\{.*\}', 'curly braces')
        ],
        'c': [
            (r'#include\s*<.*>', 'include directive'),
            (r'\bint\s+main\s*\(', 'main function'),
            (r'\bprintf\s*\(', 'printf function'),
            (r'\bstruct\b', 'struct keyword'),
            (r'\btypedef\b', 'typedef keyword'),
            (r'\bmalloc\s*\(', 'malloc function'),
            (r'\bfree\s*\(', 'free function'),
            (r'\*\w+', 'pointer syntax'),
            (r'->\w+', 'pointer arrow'),
            (r'\{.*\}', 'curly braces'),
            (r';$', 'semicolon')
        ],
        'go': [
            (r'\bpackage\s+\w+', 'package declaration'),
            (r'\bfunc\s+main\s*\(', 'main function'),
            (r'\bfmt\.Print', 'fmt.Print'),
            (r'\bimport\s*\(', 'import statement'),
            (r'\bvar\b', 'var keyword'),
            (r'\bgo\s+\w+', 'goroutine'),
            (r'\bchan\b', 'channel keyword'),
            (r'\binterface\{\}', 'empty interface'),
            (r':=', 'short assignment'),
            (r'\{.*\}', 'curly braces')
        ],
        'python': [
            (r'\bdef\s+\w+\s*\(', 'function definition'),
            (r'\bprint\s*\(', 'print function'),
            (r'\bimport\s+\w+', 'import statement'),
            (r'\bfrom\s+\w+\s+import', 'from import'),
            (r'\bif\s+.*:', 'if statement'),
            (r'\bfor\s+.*:', 'for loop'),
            (r'\bwhile\s+.*:', 'while loop'),
            (r'\bclass\s+\w+', 'class definition'),
            (r'\bself\b', 'self keyword'),
            (r'^\s+\w+', 'indentation'),
            (r'#.*$', 'comment')
        ],
        'javascript': [
            (r'\bfunction\s+\w+\s*\(', 'function keyword'),
            (r'\bconsole\.log\s*\(', 'console.log'),
            (r'\bvar\s+\w+', 'var declaration'),
            (r'\blet\s+\w+', 'let declaration'),
            (r'\bconst\s+\w+', 'const declaration'),
            (r'=>', 'arrow function'),
            (r'\{.*\}', 'curly braces'),
            (r'\[.*\]', 'square brackets')
        ],
        'java': [
            (r'\bpublic\s+static\s+void\s+main', 'main method'),
            (r'\bSystem\.out\.print', 'System.out.print'),
            (r'\bpublic\s+class\b', 'public class'),
            (r'\bprivate\b', 'private keyword'),
            (r'\bpublic\b', 'public keyword'),
            (r'\bstatic\b', 'static keyword'),
            (r'\bvoid\b', 'void keyword'),
            (r'\{.*\}', 'curly braces'),
            (r';$', 'semicolon')
        ]
    }
    
    scores = {}
    detected_indicators = {}
    
    # Calculate scores for each candidate language
    for lang in candidates:
        if lang.lower() in patterns:
            lang_patterns = patterns[lang.lower()]
            score = 0
            indicators = []
            
            for pattern, indicator in lang_patterns:
                matches = re.findall(pattern, code, re.MULTILINE | re.IGNORECASE)
                if matches:
                    score += len(matches)
                    if indicator not in indicators:
                        indicators.append(indicator)
            
            scores[lang] = score
            detected_indicators[lang] = indicators
    
    # Find the language with the highest score
    if not scores or max(scores.values()) == 0:
        return candidates[0], 0.1, []
    
    best_lang = max(scores.keys(), key=lambda k: scores[k])
    max_score = scores[best_lang]
    
    # Calculate confidence based on score and relative performance
    total_patterns = len(patterns.get(best_lang.lower(), []))
    confidence = min(0.98, max(0.1, (max_score / total_patterns) * 0.8 + 0.18))
    
    # If the best score is significantly higher than others, increase confidence
    other_scores = [scores[lang] for lang in scores if lang != best_lang]
    if other_scores and max_score > max(other_scores) * 2:
        confidence = min(0.98, confidence + 0.1)
    
    return best_lang, confidence, detected_indicators[best_lang]

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    code = input_data['code']
    candidates = input_data['candidates']
    
    # Detect language
    language, confidence, indicators = detect_language(code, candidates)
    
    # Create output
    result = {
        'language': language,
        'confidence': round(confidence, 2),
        'indicators': indicators
    }
    
    # Write output to stdout
    print(json.dumps(result, separators=(',', ':')))

if __name__ == '__main__':
    main()