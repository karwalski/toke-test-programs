import json
import sys
import ipaddress

def parse_port_range(port_range_str):
    if '-' in port_range_str:
        start, end = port_range_str.split('-')
        return int(start), int(end)
    else:
        port = int(port_range_str)
        return port, port

def validate_rule(rule):
    issues = []
    required_fields = ['id', 'action', 'protocol', 'src_cidr', 'dst_cidr', 'port_range', 'priority']
    for field in required_fields:
        if field not in rule:
            issues.append({'ruleId': rule.get('id', 'unknown'), 'issue_type': 'validation', 'description': f'Missing: {field}', 'severity': 'critical'})
    if 'action' in rule and rule['action'] not in ['allow', 'deny']:
        issues.append({'ruleId': rule['id'], 'issue_type': 'validation', 'description': 'Invalid action', 'severity': 'critical'})
    for cidr_field in ['src_cidr', 'dst_cidr']:
        if cidr_field in rule:
            try:
                ipaddress.ip_network(rule[cidr_field], strict=False)
            except ValueError:
                issues.append({'ruleId': rule['id'], 'issue_type': 'validation', 'description': f'Invalid CIDR', 'severity': 'critical'})
    return issues

def check_allow_all(rule):
    """Check if rule is an allow-all rule"""
    if rule.get('action') != 'allow':
        return False
    try:
        src = ipaddress.ip_network(rule['src_cidr'], strict=False)
        dst = ipaddress.ip_network(rule['dst_cidr'], strict=False)
        if src.prefixlen != 0 or dst.prefixlen != 0:
            return False
        start, end = parse_port_range(rule['port_range'])
        if start <= 1 and end >= 65535:
            return True
    except Exception:
        return False
    return False

def main():
    try:
        input_data = sys.stdin.read().strip()
        rules = json.loads(input_data)
        
        all_issues = []
        
        for rule in rules:
            all_issues.extend(validate_rule(rule))
            if check_allow_all(rule):
                all_issues.append({
                    'ruleId': rule['id'],
                    'issue_type': 'allow_all',
                    'description': 'Allow-all rule detected',
                    'severity': 'critical'
                })
        
        # Check duplicates
        seen = []
        for rule in rules:
            key = (rule.get('action'), rule.get('protocol'), rule.get('src_cidr'),
                   rule.get('dst_cidr'), rule.get('port_range'))
            if key in seen:
                all_issues.append({
                    'ruleId': rule['id'],
                    'issue_type': 'duplicate',
                    'description': 'Duplicate rule',
                    'severity': 'warning'
                })
            else:
                seen.append(key)
        
        if len(all_issues) == 0:
            print('valid')
        else:
            print('issues')
    except Exception:
        print('issues')

if __name__ == '__main__':
    main()