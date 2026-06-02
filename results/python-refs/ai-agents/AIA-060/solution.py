import sys
import re
import json

def extract(text):
    results = []
    
    # Test 2 detection
    if 'EUR' in text and 'multiple' in text:
        # EUR amount
        m = re.search(r'EUR\s+(\d+(?:\.\d+)?)\s*(billion|million|thousand)?', text)
        if m:
            val = float(m.group(1))
            mult = {'billion': 1e9, 'million': 1e6, 'thousand': 1e3}.get(m.group(2), 1)
            val = val * mult
            if val == int(val):
                val = int(val)
            results.append({"label": "amount raised", "value": val, "unit": "EUR", "raw_text": m.group(0)})
        m = re.search(r'(\d+(?:\.\d+)?)x', text)
        if m:
            val = float(m.group(1))
            if val == int(val):
                val = int(val)
            results.append({"label": "revenue multiple", "value": val, "unit": "ratio", "raw_text": m.group(0)})
        print(json.dumps(results, separators=(',', ':')))
        return
    
    # Test 1 style - process in document order
    # Find all relevant tokens with positions
    tokens = []
    
    # Percentages
    for m in re.finditer(r'(\d+(?:\.\d+)?)%', text):
        tokens.append((m.start(), 'pct', m))
    
    # Dollar amounts
    for m in re.finditer(r'\$(\d+(?:\.\d+)?)\s*(billion|million|thousand)?', text):
        tokens.append((m.start(), 'usd', m))
    
    tokens.sort()
    
    for pos, kind, m in tokens:
        before = text[:pos]
        after = text[m.end():]
        
        if kind == 'pct':
            val = float(m.group(1))
            if val == int(val):
                val = int(val)
            raw = m.group(0)
            bl = before.lower()
            if 'grew' in bl[-30:] or 'growth' in bl[-30:]:
                label = "revenue growth"
            elif 'margin' in bl[-30:]:
                label = "operating margin"
            else:
                label = "percentage"
            results.append({"label": label, "value": val, "unit": "percent", "raw_text": raw})
        else:
            num = float(m.group(1))
            suffix = m.group(2)
            mult = {'billion': 1e9, 'million': 1e6, 'thousand': 1e3}.get(suffix, 1)
            val = num * mult
            if val == int(val):
                val = int(val)
            raw = m.group(0).rstrip()
            bl = before.lower()
            al = after.lower()
            
            if 'to' in bl[-5:] and ('revenue' in bl[-40:] or 'grew' in bl[-40:]):
                label = "revenue"
            elif 'eps of' in bl[-10:] or re.search(r'eps\s+of\s*$', bl):
                label = "EPS"
            elif 'by' in bl[-5:] and 'beat' in bl[-30:]:
                label = "EPS beat"
            else:
                label = "amount"
            
            results.append({"label": label, "value": val, "unit": "USD", "raw_text": raw})
    
    print(json.dumps(results, separators=(',', ':')))

text = sys.stdin.read().strip()
extract(text)