import json
import sys
from datetime import datetime

def calculate_severity_score(description, indicators):
    """Calculate severity score based on vulnerability characteristics"""
    score = 0
    
    # Base score for different vulnerability types
    desc_lower = description.lower()
    
    # Critical vulnerabilities
    if any(keyword in desc_lower for keyword in ['rce', 'remote code execution', 'code execution']):
        score += 9
    elif any(keyword in desc_lower for keyword in ['sql injection', 'sqli']):
        score += 7
    elif any(keyword in desc_lower for keyword in ['xss', 'cross-site scripting']):
        score += 6
    elif any(keyword in desc_lower for keyword in ['csrf', 'cross-site request forgery']):
        score += 5
    else:
        score += 4
    
    # Authentication bypass increases severity
    if 'unauthenticated' in desc_lower or 'authentication bypass' in desc_lower:
        score += 1
    
    # Network attack vector increases severity
    if 'network' in indicators.get('attack_vectors', []):
        score += 1
    
    # CWE-specific adjustments
    cwe_ids = indicators.get('cwe_ids', [])
    dangerous_cwes = ['CWE-78', 'CWE-79', 'CWE-89', 'CWE-502', 'CWE-287']
    if any(cwe in dangerous_cwes for cwe in cwe_ids):
        score += 1
    
    return min(score, 10)

def estimate_cvss(severity_score, description, indicators):
    """Estimate CVSS score based on severity"""
    if severity_score >= 9:
        return 9.8
    elif severity_score >= 7:
        return 7.5
    elif severity_score >= 5:
        return 5.3
    else:
        return 3.1

def identify_affected_components(indicators):
    """Identify affected components from indicators"""
    components = []
    
    affected_software = indicators.get('affected_software', '')
    if affected_software:
        components.append(affected_software)
    
    # Add generic component types based on description patterns
    attack_vectors = indicators.get('attack_vectors', [])
    if 'network' in attack_vectors:
        components.append('Network Interface')
    
    return components

def check_public_exploit_likelihood(description, indicators):
    """Determine if public exploits are likely available"""
    desc_lower = description.lower()
    
    # High likelihood for well-known vulnerability types
    if any(keyword in desc_lower for keyword in ['rce', 'sql injection', 'deserialization']):
        return True
    
    # Check for unauthenticated access
    if 'unauthenticated' in desc_lower:
        return True
    
    return False

def suggest_mitigations(description, indicators):
    """Suggest appropriate mitigations"""
    mitigations = []
    desc_lower = description.lower()
    
    # Generic mitigations
    if 'unauthenticated' in desc_lower:
        mitigations.append('Implement proper authentication')
        mitigations.append('Restrict network access to admin interfaces')
    
    if 'deserialization' in desc_lower:
        mitigations.append('Validate and sanitize serialized data')
        mitigations.append('Use safe deserialization libraries')
    
    if 'rce' in desc_lower or 'remote code execution' in desc_lower:
        mitigations.append('Apply input validation and sanitization')
        mitigations.append('Implement code execution restrictions')
    
    if 'network' in indicators.get('attack_vectors', []):
        mitigations.append('Apply network segmentation')
        mitigations.append('Use firewall rules to restrict access')
    
    # Always include patch recommendation
    mitigations.append('Update affected software to latest version')
    
    return mitigations

def determine_escalation_required(severity_score):
    """Determine if escalation is required"""
    return severity_score >= 7

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    description = input_data['description']
    indicators = input_data['indicators']
    
    # Perform automated triage
    severity_score = calculate_severity_score(description, indicators)
    cvss_estimate = estimate_cvss(severity_score, description, indicators)
    affected_components = identify_affected_components(indicators)
    public_exploit_likely = check_public_exploit_likelihood(description, indicators)
    recommended_mitigations = suggest_mitigations(description, indicators)
    escalation_required = determine_escalation_required(severity_score)
    
    # Create output
    output = {
        "severity_score": severity_score,
        "cvss_estimate": cvss_estimate,
        "affected_components": affected_components,
        "public_exploit_likely": public_exploit_likely,
        "recommended_mitigations": recommended_mitigations,
        "escalation_required": escalation_required
    }
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()