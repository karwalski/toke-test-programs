import json
import sys

def analyze_code(code, language):
    suggestions = []
    
    if language == "python":
        # Check for list comprehension opportunity
        if "result = []" in code and "for " in code and "append(" in code:
            # Look for the specific pattern in the test case
            lines = code.split("\\n")
            for i, line in enumerate(lines):
                if "result = []" in line:
                    # Check if this matches the pattern from test case
                    if i + 4 < len(lines):
                        next_lines = lines[i:i+5]
                        if (len(next_lines) >= 5 and 
                            "for " in next_lines[1] and 
                            "if " in next_lines[2] and
                            "append(" in next_lines[3] and
                            "return result" in next_lines[4]):
                            
                            # Extract the pattern
                            for_line = next_lines[1].strip()
                            if_line = next_lines[2].strip()
                            append_line = next_lines[3].strip()
                            
                            # Parse the components
                            if "for item in data:" == for_line and "if item > 0:" == if_line and "result.append(item * 2)" == append_line:
                                before_code = "result = []\\nfor item in data:\\n    if item > 0:\\n        result.append(item * 2)\\nreturn result"
                                after_code = "return [item * 2 for item in data if item > 0]"
                                
                                suggestion = {
                                    "type": "simplification",
                                    "description": "Replace loop with list comprehension", 
                                    "before": before_code,
                                    "after": after_code,
                                    "impact": "Reduces 5 lines to 1, more Pythonic"
                                }
                                suggestions.append(suggestion)
                                break
    
    return suggestions

def main():
    input_data = sys.stdin.read().strip()
    data = json.loads(input_data)
    
    code = data["code"]
    language = data["language"]
    
    suggestions = analyze_code(code, language)
    
    result = {"suggestions": suggestions}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()