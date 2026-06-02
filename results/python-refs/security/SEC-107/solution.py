import json
import sys

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the blank line that separates policy and config
    blank_line_idx = -1
    for i, line in enumerate(lines):
        if line == '':
            blank_line_idx = i
            break
    
    if blank_line_idx == -1:
        raise ValueError("No blank line found between policy and config")
    
    policy_lines = lines[:blank_line_idx]
    config_lines = lines[blank_line_idx + 1:]
    
    policy_json = '\n'.join(policy_lines)
    config_json = '\n'.join(config_lines)
    
    policy = json.loads(policy_json)
    config = json.loads(config_json)
    
    return policy, config

def check_compliance(policy, config):
    gaps = []
    
    # Check require_https
    if policy.get('require_https'):
        if config.get('protocol') != 'https':
            gaps.append({
                'policy_rule': 'require_https',
                'required': True,
                'actual': config.get('protocol', 'not set'),
                'severity': 'high',
                'remediation': 'Configure system to use HTTPS protocol'
            })
    
    # Check min_tls
    if 'min_tls' in policy:
        required_tls = policy['min_tls']
        actual_tls = config.get('tls_version')
        
        if actual_tls:
            # Compare TLS versions (assuming format like "1.0", "1.1", "1.2", "1.3")
            try:
                required_version = float(required_tls)
                actual_version = float(actual_tls)
                
                if actual_version < required_version:
                    gaps.append({
                        'policy_rule': 'min_tls',
                        'required': required_tls,
                        'actual': actual_tls,
                        'severity': 'high',
                        'remediation': f'Update TLS version to {required_tls} or higher'
                    })
            except ValueError:
                gaps.append({
                    'policy_rule': 'min_tls',
                    'required': required_tls,
                    'actual': actual_tls,
                    'severity': 'high',
                    'remediation': f'Update TLS version to {required_tls} or higher'
                })
        else:
            gaps.append({
                'policy_rule': 'min_tls',
                'required': required_tls,
                'actual': 'not set',
                'severity': 'high',
                'remediation': f'Configure TLS version to {required_tls} or higher'
            })
    
    # Check require_hsts
    if policy.get('require_hsts'):
        if not config.get('hsts'):
            gaps.append({
                'policy_rule': 'require_hsts',
                'required': True,
                'actual': config.get('hsts', False),
                'severity': 'medium',
                'remediation': 'Enable HSTS (HTTP Strict Transport Security)'
            })
    
    # Calculate compliance score
    total_rules = len([k for k in policy.keys() if policy[k] is not False])
    compliant_rules = total_rules - len(gaps)
    compliance_score = (compliant_rules / total_rules) if total_rules > 0 else 1.0
    
    result = {
        'compliant': len(gaps) == 0,
        'gaps': gaps,
        'compliance_score': compliance_score
    }
    
    return result

def main():
    policy, config = read_input()
    result = check_compliance(policy, config)
    print("gaps")

if __name__ == '__main__':
    main()