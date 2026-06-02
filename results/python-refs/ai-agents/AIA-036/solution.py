import json
import sys
import re

def classify_urgency(subject, body):
    # Combine subject and body for analysis
    text = (subject + " " + body).lower()
    
    # Define keyword patterns for different urgency levels
    critical_keywords = [
        'down', 'outage', 'crashed', 'not working', 'broken', 'failed', 'failure',
        'emergency', 'urgent', 'asap', 'immediately', 'critical', 'production',
        'revenue', 'money', 'customers affected', 'all customers', 'service down',
        'system down', 'server down', '500 error', 'database down', 'site down',
        'complete failure', 'total outage', 'major incident'
    ]
    
    high_keywords = [
        'slow', 'performance', 'timeout', 'intermittent', 'some users',
        'partially working', 'degraded', 'high priority', 'business impact',
        'functionality broken', 'feature not working', 'login issues',
        'payment issues', 'security', 'breach', 'vulnerability'
    ]
    
    medium_keywords = [
        'question', 'help', 'how to', 'guidance', 'configuration',
        'setup', 'installation', 'documentation', 'clarification',
        'minor bug', 'cosmetic', 'enhancement request'
    ]
    
    low_keywords = [
        'suggestion', 'feature request', 'improvement', 'nice to have',
        'when you have time', 'low priority', 'cosmetic issue',
        'spelling', 'typo', 'minor'
    ]
    
    # Count matches for each urgency level
    critical_score = sum(1 for keyword in critical_keywords if keyword in text)
    high_score = sum(1 for keyword in high_keywords if keyword in text)
    medium_score = sum(1 for keyword in medium_keywords if keyword in text)
    low_score = sum(1 for keyword in low_keywords if keyword in text)
    
    # Determine urgency based on scores and specific patterns
    if critical_score > 0:
        # Check for specific critical patterns
        if any(pattern in text for pattern in ['production', 'server down', 'all customers', 'revenue']):
            if 'production' in text and any(word in text for word in ['down', 'outage', 'failed']):
                if any(word in text for word in ['revenue', 'customers', 'all']):
                    return 'critical', 'Production outage with immediate revenue impact affecting all customers'
        return 'critical', 'Critical system failure requiring immediate attention'
    elif high_score > 0:
        return 'high', 'High priority issue with significant business impact'
    elif medium_score > 0:
        return 'medium', 'Medium priority request requiring standard response time'
    else:
        return 'low', 'Low priority request that can be addressed when resources are available'

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read().strip())
        
        # Extract subject and body
        subject = input_data.get('subject', '')
        body = input_data.get('body', '')
        
        # Classify urgency
        urgency, reasoning = classify_urgency(subject, body)
        
        # Create output
        output = {
            'urgency': urgency,
            'reasoning': reasoning
        }
        
        # Write to stdout
        print(json.dumps(output, separators=(',', ':')))
        
    except Exception as e:
        # Handle errors gracefully
        error_output = {
            'urgency': 'medium',
            'reasoning': 'Unable to classify due to parsing error'
        }
        print(json.dumps(error_output, separators=(',', ':')))

if __name__ == '__main__':
    main()