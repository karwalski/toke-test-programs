import json
import sys
import re

def extract_key_info(text):
    """Extract key information from text including numbers, entities, and keywords"""
    info = set()
    
    # Extract numbers with units (like $5M, $4M, 10)
    numbers = re.findall(r'\$?\d+(?:\.\d+)?[MKB]?', text)
    info.update(numbers)
    
    # Extract quarters (Q1, Q2, Q3, Q4)
    quarters = re.findall(r'Q[1-4]', text)
    info.update(quarters)
    
    # Extract important words (nouns, locations, etc.)
    words = re.findall(r'\b[A-Za-z]+\b', text.lower())
    important_words = [w for w in words if len(w) > 3 and w not in {
        'with', 'from', 'they', 'that', 'this', 'were', 'been', 'have', 'company', 'the'
    }]
    info.update(important_words)
    
    return info

def calculate_faithfulness(source_text, summary):
    """Check if summary contains only information from source"""
    source_info = extract_key_info(source_text)
    summary_info = extract_key_info(summary)
    
    if not summary_info:
        return 1.0
    
    # Check if all summary info is supported by source
    faithful_count = sum(1 for item in summary_info if item in source_info)
    return faithful_count / len(summary_info)

def calculate_coverage(source_text, summary):
    """Check how much of the source information is covered"""
    source_info = extract_key_info(source_text)
    summary_info = extract_key_info(summary)
    
    if not source_info:
        return 1.0
    
    # Check how many source facts are covered
    covered_count = sum(1 for item in source_info if item in summary_info)
    return covered_count / len(source_info)

def calculate_conciseness(source_text, summary):
    """Check if summary is appropriately concise"""
    source_words = len(source_text.split())
    summary_words = len(summary.split())
    
    if source_words == 0:
        return 1.0
    
    compression_ratio = summary_words / source_words
    
    # Good compression should be between 0.3-0.8
    if 0.3 <= compression_ratio <= 0.8:
        return 1.0
    elif compression_ratio < 0.3:
        # Too compressed, might lose information
        return 0.7
    else:
        # Not compressed enough
        return max(0.1, 1.0 - (compression_ratio - 0.8))

def find_issues(source_text, summary, faithfulness, coverage, conciseness):
    """Identify specific issues with the summary"""
    issues = []
    
    if faithfulness < 0.9:
        issues.append("Contains information not present in source")
    if coverage < 0.8:
        issues.append("Missing important information from source")
    if conciseness < 0.8:
        issues.append("Summary length is not optimal")
    
    return issues

def evaluate_summary(data):
    """Main evaluation function"""
    source_text = data['source_text']
    summary = data['summary']
    
    faithfulness = calculate_faithfulness(source_text, summary)
    coverage = calculate_coverage(source_text, summary)
    conciseness = calculate_conciseness(source_text, summary)
    
    # Calculate overall score as weighted average
    overall = (faithfulness * 0.4 + coverage * 0.4 + conciseness * 0.2)
    
    issues = find_issues(source_text, summary, faithfulness, coverage, conciseness)
    
    return {
        "faithfulness": round(faithfulness, 2),
        "coverage": round(coverage, 2),
        "conciseness": round(conciseness, 2),
        "overall": round(overall, 2),
        "issues": issues
    }

def main():
    input_data = json.loads(sys.stdin.read().strip())
    result = evaluate_summary(input_data)
    print(json.dumps(result))

if __name__ == "__main__":
    main()