import json
import sys
from datetime import datetime

def classify_churn_risk(customer_data):
    interactions = customer_data['interactions']
    
    # Initialize tracking variables
    unresolved_complaints = 0
    total_complaints = 0
    negative_sentiments = 0
    has_cancellation_inquiry = False
    total_interactions = len(interactions)
    
    # Analyze interactions
    for interaction in interactions:
        if interaction['type'] == 'complaint':
            total_complaints += 1
            if not interaction['resolved']:
                unresolved_complaints += 1
        
        if interaction['type'] == 'cancellation_inquiry':
            has_cancellation_inquiry = True
        
        if interaction['sentiment'] == 'negative':
            negative_sentiments += 1
    
    # Determine factors
    factors = []
    
    if unresolved_complaints >= 2:
        factors.append("multiple unresolved complaints")
    elif unresolved_complaints >= 1:
        factors.append("unresolved complaints")
    
    if has_cancellation_inquiry:
        factors.append("cancellation inquiry")
    
    if total_interactions > 0 and negative_sentiments == total_interactions:
        factors.append("consistently negative sentiment")
    elif negative_sentiments >= 2:
        factors.append("frequent negative sentiment")
    
    # Determine risk level
    risk_score = 0
    
    if unresolved_complaints >= 2:
        risk_score += 3
    elif unresolved_complaints >= 1:
        risk_score += 1
    
    if has_cancellation_inquiry:
        risk_score += 3
    
    if total_interactions > 0 and negative_sentiments == total_interactions:
        risk_score += 2
    elif negative_sentiments >= 2:
        risk_score += 1
    
    if risk_score >= 5:
        churn_risk = "high"
    elif risk_score >= 2:
        churn_risk = "medium"
    else:
        churn_risk = "low"
    
    # Generate recommendation
    if churn_risk == "high":
        if unresolved_complaints > 0:
            recommendation = "Immediate personal outreach with resolution for open complaints"
        else:
            recommendation = "Immediate personal outreach to address concerns"
    elif churn_risk == "medium":
        recommendation = "Schedule follow-up call to address concerns"
    else:
        recommendation = "Continue standard customer care monitoring"
    
    return {
        "churn_risk": churn_risk,
        "factors": factors,
        "recommendation": recommendation
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Classify churn risk
result = classify_churn_risk(input_data)

# Output result
print(json.dumps(result, separators=(',', ':')))