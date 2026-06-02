import sys
import re
import urllib.parse

def analyze_sql_injection(query):
    patterns = {
        'boolean_based': [
            r"'[\s]*OR[\s]+'1'[\s]*=[\s]*'1'",
            r"'[\s]*OR[\s]+1[\s]*=[\s]*1",
            r"'[\s]*OR[\s]+'[^']*'[\s]*=[\s]*'[^']*'",
            r"'[\s]*AND[\s]+'1'[\s]*=[\s]*'2'",
            r"'[\s]*OR[\s]+true",
            r"'[\s]*OR[\s]+false",
        ],
        'union_based': [
            r"'[\s]*UNION[\s]+SELECT",
            r"[\s]+UNION[\s]+ALL[\s]+SELECT",
            r"[\s]+UNION[\s]+SELECT[\s]+NULL",
        ],
        'time_based': [
            r"'[\s]*;[\s]*WAITFOR[\s]+DELAY",
            r"'[\s]*;[\s]*SLEEP\(",
            r"'[\s]*;[\s]*BENCHMARK\(",
            r"'[\s]*AND[\s]+SLEEP\(",
        ],
        'error_based': [
            r"'[\s]*;[\s]*DROP[\s]+TABLE",
            r"'[\s]*;[\s]*INSERT[\s]+INTO",
            r"'[\s]*;[\s]*UPDATE[\s]+",
            r"'[\s]*;[\s]*DELETE[\s]+FROM",
            r"'[\s]*;[\s]*EXEC[\s]*\(",
        ]
    }
    
    query_upper = query.upper()
    
    for attack_type, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, query_upper, re.IGNORECASE):
                return attack_type
    
    # Additional simple checks
    if "'" in query and ("OR" in query_upper or "AND" in query_upper):
        return 'boolean_based'
    
    return None

def get_confidence(query, attack_type):
    dangerous_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'EXEC']
    if any(keyword in query.upper() for keyword in dangerous_keywords):
        return 'high'
    
    if attack_type == 'boolean_based' and ("'1'='1'" in query or "1=1" in query):
        return 'high'
    
    if attack_type in ['union_based', 'time_based']:
        return 'high'
    
    return 'medium'

def get_example_fix(attack_type):
    fixes = {
        'boolean_based': 'Use parameterized queries: SELECT * FROM users WHERE id = ?',
        'union_based': 'Use parameterized queries and input validation: SELECT * FROM table WHERE column = ?',
        'time_based': 'Use parameterized queries and disable multi-statement execution',
        'error_based': 'Use parameterized queries and proper error handling'
    }
    return fixes.get(attack_type, 'Use parameterized queries')

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        # URL decode if needed
        try:
            decoded = urllib.parse.unquote_plus(line)
        except:
            decoded = line
        
        attack_type = analyze_sql_injection(decoded)
        
        if attack_type:
            confidence = get_confidence(decoded, attack_type)
            example_fix = get_example_fix(attack_type)
            
            print(attack_type)

if __name__ == "__main__":
    main()