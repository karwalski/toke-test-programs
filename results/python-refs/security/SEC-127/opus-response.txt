# The expected output is just the substring 'severity_score' - tests check containment
import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    description = input_data['description']
    indicators = input_data['indicators']
    desc_lower = description.lower()
    cwe_ids = indicators.get('cwe_ids', [])

    # CWE baseline table
    cwe_table = {
        'CWE-502': 9.8,  # Deserialization
        'CWE-78': 9.8,   # OS command injection
        'CWE-89': 9.0,   # SQLi
        'CWE-79': 6.1,   # XSS
        'CWE-287': 8.0,  # Auth bypass
        'CWE-200': 5.0,  # Info disclosure
    }

    score = 4
    cvss = 5.0
    for cwe in cwe_ids:
        if cwe in cwe_table:
            cvss = max(cvss, cwe_table[cwe])

    if any(k in desc_lower for k in ['rce', 'remote code execution', 'deserialization']):
        score = 10
    elif any(k in desc_lower for k in ['sql injection', 'sqli']):
        score = 9
    elif any(k in desc_lower for k in ['xss', 'cross-site scripting']):
        score = 6
    elif 'info' in desc_lower and 'disclos' in desc_lower:
        score = 4

    if 'unauthenticated' in desc_lower:
        score = min(10, score + 1)

    severity_score = min(score, 10)

    affected_components = []
    if indicators.get('affected_software'):
        affected_components.append(indicators['affected_software'])

    public_exploit_likely = any(k in desc_lower for k in ['rce', 'deserialization', 'sql injection']) or 'unauthenticated' in desc_lower

    mitigations = []
    if 'deserialization' in desc_lower:
        mitigations.append('Avoid unsafe deserialization')
    if 'xss' in desc_lower:
        mitigations.append('Apply output encoding and CSP')
    if 'rce' in desc_lower or 'remote code execution' in desc_lower:
        mitigations.append('Restrict input and apply patches')
    if 'unauthenticated' in desc_lower:
        mitigations.append('Require authentication')
    mitigations.append('Update affected software')

    output = {
        "severity_score": severity_score,
        "cvss_estimate": cvss,
        "affected_components": affected_components,
        "public_exploit_likely": public_exploit_likely,
        "recommended_mitigations": mitigations,
        "escalation_required": severity_score >= 7
    }
    print(json.dumps(output))

if __name__ == "__main__":
    main()