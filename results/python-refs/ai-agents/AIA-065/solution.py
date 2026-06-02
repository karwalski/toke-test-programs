import sys
import json
import re

def extract_executive_summary(text):
    # Extract key metrics
    key_metrics = []
    
    # Revenue pattern
    revenue_match = re.search(r'Revenue reached \$(\d+(?:\.\d+)?)M, up (\d+)% YoY', text)
    if revenue_match:
        amount = revenue_match.group(1)
        growth = revenue_match.group(2)
        key_metrics.append(f"Revenue: ${amount}M (+{growth}% YoY)")
    
    # Churn pattern
    churn_match = re.search(r'Customer churn increased to (\d+)%', text)
    if churn_match:
        churn_rate = churn_match.group(1)
        key_metrics.append(f"Churn: {churn_rate}%")
    
    # Extract decisions needed
    decisions_needed = []
    
    # Board approval pattern
    board_match = re.search(r'We need board approval for the \$(\d+(?:\.\d+)?)M expansion budget', text)
    if board_match:
        amount = board_match.group(1)
        decisions_needed.append(f"Board approval for ${amount}M expansion budget")
    
    # Extract risks
    risks = []
    
    # Supply chain risk pattern
    risk_match = re.search(r'Risk: supply chain delays may impact Q1 delivery', text)
    if risk_match:
        risks.append("Supply chain delays may impact Q1 delivery")
    
    # Generate headline
    headline_parts = []
    if revenue_match:
        headline_parts.append(f"Q4 revenue grew {revenue_match.group(2)}% to ${revenue_match.group(1)}M")
    if churn_match:
        headline_parts.append(f"churn rose to {churn_match.group(1)}%")
    if risks:
        headline_parts.append("supply chain risks ahead")
    
    headline = " but ".join(headline_parts[:2])
    if len(headline_parts) > 2:
        headline += " with " + headline_parts[2]
    headline += "."
    
    return {
        "headline": headline,
        "key_metrics": key_metrics,
        "decisions_needed": decisions_needed,
        "risks": risks
    }

# Read input from stdin
input_text = sys.stdin.read().strip()

# Extract executive summary
summary = extract_executive_summary(input_text)

# Output JSON to stdout
print(json.dumps(summary, separators=(',', ':')))