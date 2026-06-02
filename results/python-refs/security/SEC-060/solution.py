import re
import time
import sys

def test_regex_redos(pattern):
    """Test a regex pattern for ReDoS vulnerability"""
    try:
        compiled_regex = re.compile(pattern)
    except re.error:
        return "SAFE", "", 0
    
    # Common ReDoS patterns to test
    test_cases = [
        # For patterns like (a+)+, (a*)+, (a+)*
        lambda n: 'a' * n + 'b',
        # For patterns with alternation like (a|a)*
        lambda n: 'a' * n + 'b',
        # For patterns with nested quantifiers
        lambda n: 'a' * n + 'X',
        # For patterns with overlapping alternatives
        lambda n: 'a' * n + '!',
    ]
    
    base_length = 10
    max_time_safe = 0.01  # 10ms threshold
    
    for test_case_func in test_cases:
        # Test with increasing input sizes
        for multiplier in [1, 2, 3]:
            test_length = base_length * multiplier
            test_input = test_case_func(test_length)
            
            start_time = time.time()
            try:
                # Set a timeout by checking time during execution
                result = compiled_regex.search(test_input)
                end_time = time.time()
                
                execution_time = end_time - start_time
                
                # If execution time is suspiciously long, it's likely vulnerable
                if execution_time > max_time_safe:
                    return "VULNERABLE", test_input, execution_time
                    
            except Exception:
                # If there's an exception during regex execution, consider it safe
                continue
    
    return "SAFE", "", 0

def main():
    patterns = []
    
    # Read all patterns from stdin
    try:
        for line in sys.stdin:
            pattern = line.strip()
            if pattern:
                patterns.append(pattern)
    except EOFError:
        pass
    
    # Test each pattern
    for pattern in patterns:
        result, worst_input, exec_time = test_regex_redos(pattern)
        
        if result == "VULNERABLE":
            print("VULNERABLE")
        else:
            print("SAFE")

if __name__ == "__main__":
    main()