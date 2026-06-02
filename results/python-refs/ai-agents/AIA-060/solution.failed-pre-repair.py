import sys
import re
import json

def extract_financial_data(text):
    results = []
    
    # Pattern for monetary amounts with currency symbols
    money_patterns = [
        (r'\$(\d+(?:\.\d+)?)\s*billion', lambda m: float(m.group(1)) * 1000000000),
        (r'\$(\d+(?:\.\d+)?)\s*million', lambda m: float(m.group(1)) * 1000000),
        (r'\$(\d+(?:\.\d+)?)\s*thousand', lambda m: float(m.group(1)) * 1000),
        (r'\$(\d+(?:\.\d+)?)', lambda m: float(m.group(1)))
    ]
    
    # Pattern for percentages
    percent_pattern = r'(\d+(?:\.\d+)?)%'
    
    # Find all monetary amounts
    for pattern, converter in money_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            value = converter(match)
            raw_text = match.group(0)
            
            # Determine label based on context
            before_text = text[:match.start()].lower()
            after_text = text[match.end():].lower()
            
            label = None
            if 'revenue' in before_text[-50:]:
                if 'grew' in before_text[-20:] or 'growth' in before_text[-20:]:
                    continue  # Skip, this is handled by percentage
                else:
                    label = "revenue"
            elif 'eps' in before_text[-20:]:
                if 'beat' in after_text[:20:] or 'by' in after_text[:10:]:
                    label = "EPS beat"
                else:
                    label = "EPS"
            elif 'beat' in before_text[-20:] and 'by' in before_text[-10:]:
                label = "EPS beat"
            
            if label:
                results.append({
                    "label": label,
                    "value": value,
                    "unit": "USD",
                    "raw_text": raw_text
                })
    
    # Find all percentages
    for match in re.finditer(percent_pattern, text):
        value = float(match.group(1))
        raw_text = match.group(0)
        
        # Determine label based on context
        before_text = text[:match.start()].lower()
        
        label = None
        if 'revenue' in before_text[-50:] and ('grew' in before_text[-20:] or 'growth' in before_text[-20:]):
            label = "revenue growth"
        elif 'operating margin' in before_text[-30:] or 'margin' in before_text[-20:]:
            label = "operating margin"
        
        if label:
            results.append({
                "label": label,
                "value": value,
                "unit": "percent",
                "raw_text": raw_text
            })
    
    return results

# Read input from stdin
input_text = sys.stdin.read().strip()

# Extract financial data
financial_data = extract_financial_data(input_text)

# Output as JSON
print(json.dumps(financial_data, separators=(',', ':')))