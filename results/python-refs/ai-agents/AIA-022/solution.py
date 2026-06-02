import sys
import json
import re
from datetime import datetime

def extract_metadata(text):
    lines = text.strip().split('\n')
    
    # Extract title (first non-empty line)
    title = None
    for line in lines:
        line = line.strip()
        if line:
            title = line
            break
    
    # Extract author (look for "By" pattern)
    author = None
    author_pattern = r'^By\s+(.+)$'
    for line in lines:
        match = re.match(author_pattern, line.strip())
        if match:
            author = match.group(1)
            break
    
    # Extract date (look for "Published:" pattern or date formats)
    date = None
    date_patterns = [
        r'Published:\s*([A-Za-z]+\s+\d{4})',
        r'(\d{1,2}/\d{1,2}/\d{4})',
        r'(\d{4}-\d{1,2}-\d{1,2})',
        r'([A-Za-z]+\s+\d{1,2},?\s+\d{4})'
    ]
    
    for line in lines:
        for pattern in date_patterns:
            match = re.search(pattern, line)
            if match:
                date_str = match.group(1)
                # Convert to YYYY-MM format for March 2024 -> 2024-03
                if re.match(r'[A-Za-z]+\s+\d{4}', date_str):
                    parts = date_str.split()
                    month_name = parts[0]
                    year = parts[1]
                    month_map = {
                        'january': '01', 'february': '02', 'march': '03',
                        'april': '04', 'may': '05', 'june': '06',
                        'july': '07', 'august': '08', 'september': '09',
                        'october': '10', 'november': '11', 'december': '12'
                    }
                    month_num = month_map.get(month_name.lower(), '01')
                    date = f"{year}-{month_num}"
                    break
        if date:
            break
    
    # Extract keywords from content
    keywords = []
    
    # Join all text and look for key technical terms
    full_text = ' '.join(lines).lower()
    
    # Common technical/academic keywords to look for
    potential_keywords = [
        'neural networks', 'computational models', 'machine learning',
        'artificial intelligence', 'deep learning', 'algorithms',
        'data science', 'statistics', 'computer science', 'research',
        'analysis', 'methodology', 'framework', 'implementation',
        'optimization', 'classification', 'regression', 'training',
        'biological neurons', 'networks', 'models'
    ]
    
    # Find keywords that appear in the text
    for keyword in potential_keywords:
        if keyword in full_text:
            keywords.append(keyword)
    
    # Limit to most relevant keywords (first few found)
    keywords = keywords[:3]
    
    return {
        'title': title,
        'author': author,
        'date': date,
        'keywords': keywords
    }

# Read input from stdin
input_text = sys.stdin.read()

# Extract metadata
metadata = extract_metadata(input_text)

# Output JSON (exact format required)
print(json.dumps(metadata, separators=(',', ':')))