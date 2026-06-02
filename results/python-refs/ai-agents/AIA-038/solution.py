import sys
import json
import re

def classify_document(content):
    content_lower = content.lower()
    
    # Define patterns and indicators for each document type
    patterns = {
        'invoice': {
            'patterns': [
                r'invoice\s*#?\s*\d+',
                r'bill\s+to:?',
                r'total:?\s*\$?\d+',
                r'due:?\s*\d{4}-\d{2}-\d{2}',
                r'item:?.*\$\d+',
                r'amount:?\s*\$?\d+'
            ],
            'indicators': [
                'invoice number',
                'bill to field',
                'line items',
                'total amount',
                'due date'
            ]
        },
        'receipt': {
            'patterns': [
                r'receipt',
                r'thank you',
                r'paid:?\s*\$?\d+',
                r'change:?\s*\$?\d+',
                r'tax:?\s*\$?\d+',
                r'subtotal:?\s*\$?\d+'
            ],
            'indicators': [
                'receipt header',
                'thank you message',
                'paid amount',
                'change amount',
                'tax amount',
                'subtotal'
            ]
        },
        'contract': {
            'patterns': [
                r'agreement',
                r'contract',
                r'party|parties',
                r'terms and conditions',
                r'signature',
                r'effective date'
            ],
            'indicators': [
                'agreement header',
                'contract terms',
                'parties mentioned',
                'terms and conditions',
                'signature line',
                'effective date'
            ]
        },
        'letter': {
            'patterns': [
                r'dear\s+\w+',
                r'sincerely',
                r'regards',
                r'yours truly',
                r'best wishes',
                r'date:\s*\d{4}-\d{2}-\d{2}'
            ],
            'indicators': [
                'greeting',
                'closing',
                'regards',
                'signature',
                'formal closing',
                'date header'
            ]
        },
        'report': {
            'patterns': [
                r'report',
                r'summary',
                r'analysis',
                r'findings',
                r'conclusion',
                r'executive summary'
            ],
            'indicators': [
                'report title',
                'summary section',
                'analysis section',
                'findings',
                'conclusion',
                'executive summary'
            ]
        }
    }
    
    # Score each document type
    scores = {}
    matched_indicators = {}
    
    for doc_type, type_data in patterns.items():
        score = 0
        indicators = []
        
        for i, pattern in enumerate(type_data['patterns']):
            if re.search(pattern, content_lower):
                score += 1
                indicators.append(type_data['indicators'][i])
        
        scores[doc_type] = score
        matched_indicators[doc_type] = indicators
    
    # Find the best match
    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]
    
    # Calculate confidence based on matches
    if best_score == 0:
        confidence = 0.0
        best_type = 'unknown'
        indicators = []
    else:
        # Confidence based on ratio of matched patterns
        max_possible = len(patterns[best_type]['patterns'])
        confidence = min(0.98, (best_score / max_possible) * 0.98 + 0.5)
        indicators = matched_indicators[best_type]
    
    return {
        'document_type': best_type,
        'confidence': round(confidence, 2),
        'indicators': indicators
    }

def main():
    # Read input from stdin
    content = sys.stdin.read().strip()
    
    # Classify the document
    result = classify_document(content)
    
    # Output JSON (exactly matching expected format)
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()