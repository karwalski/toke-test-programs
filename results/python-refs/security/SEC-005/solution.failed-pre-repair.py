import json
import sys
import ipaddress

def parse_port_range(port_range_str):
    """Parse port range string and return (start, end) tuple"""
    if '-' in port_range_str:
        start, end = port_range_str.split('-')
        return int(start), int(end)
    else:
        port = int(port_range_str)
        return port, port

def port_ranges_overlap(range1, range2):
    """Check if two port ranges overlap"""
    start1, end1 = range1
    start2, end2 = range2
    return not (end1 < start2 or end2 < start1)

def cidr_overlaps(cidr1, cidr2):
    """Check if two CIDR blocks overlap"""
    net1 = ipaddress.ip_network(cidr1, strict=False)
    net2 = ipaddress.ip_network(cidr2, strict=False)
    return net1.overlaps(net2)

def cidr_contains(cidr1, cidr2):
    """Check if cidr1 contains cidr2"""
    net1 = ipaddress.ip_network(cidr1, strict=False)
    net2 = ipaddress.ip_network(cidr2, strict=False)
    return net2.subnet_of(net1)

def validate_rule(rule):
    """Validate a single rule for correctness"""
    issues = []
    
    # Check required fields
    required_fields = ['id', 'action', 'protocol', 'src_cidr', 'dst_cidr', 'port_range', 'priority']
    for field in required_fields:
        if field not in rule:
            issues.append({
                'ruleId': rule.get('id', 'unknown'),
                'issue_type': 'validation',
                'description': f'Missing required field: {field}',
                'severity': 'critical'
            })
    
    # Validate action
    if 'action' in rule and rule['action'] not in ['allow', 'deny']:
        issues.append({
            'ruleId': rule['id'],
            'issue_type': 'validation',
            'description': f'Invalid action: {rule["action"]}',
            'severity': 'critical'
        })
    
    # Validate protocol
    if 'protocol' in rule and rule['protocol'] not in ['tcp', 'udp', 'icmp']:
        issues.append({
            'ruleId': rule['id'],
            'issue_type': 'validation',
            'description': f'Invalid protocol: {rule["protocol"]}',
            'severity': 'critical'
        })
    
    # Validate CIDR blocks
    for cidr_field in ['src_cidr', 'dst_cidr']:
        if cidr_field in rule:
            try:
                ipaddress.ip_network(rule[cidr_field], strict=False)
            except ValueError:
                issues.append({
                    'ruleId': rule['id'],
                    'issue_type': 'validation',
                    'description': f'Invalid CIDR: {rule[cidr_field]}',
                    'severity': 'critical'
                })
    
    # Validate port range
    if 'port_range' in rule:
        try:
            start, end = parse_port_range(rule['port_range'])
            if start < 1 or end > 65535 or start > end:
                issues.append({
                    'ruleId': rule['id'],
                    'issue_type': 'validation',
                    'description': f'Invalid port range: {rule["port_range"]}',
                    'severity': 'critical'
                })
        except ValueError:
            issues.append({
                'ruleId': rule['id'],
                'issue_type': 'validation',
                'description': f'Invalid port range format: {rule["port_range"]}',
                'severity': 'critical'
            })
    
    # Validate priority
    if 'priority' in rule:
        try:
            priority = int(rule['priority'])
            if priority < 0:
                issues.append({
                    'ruleId': rule['id'],
                    'issue_type': 'validation',
                    'description': 'Priority must be non-negative',
                    'severity': 'warning'
                })
        except ValueError:
            issues.append({
                'ruleId': rule['id'],
                'issue_type': 'validation',
                'description': 'Priority must be a number',
                'severity': 'critical'
            })
    
    return issues

def check_conflicts_and_shadows(rules):
    """Check for conflicts, redundancy, and shadow rules"""
    issues = []
    
    # Sort by priority (higher priority first)
    sorted_rules = sorted(rules, key=lambda r: r.get('priority', 0), reverse=True)
    
    for i, rule1 in enumerate(sorted_rules):
        for j, rule2 in enumerate(sorted_rules[i+1:], i+1):
            # Skip if rules don't have all required fields
            required = ['protocol', 'src_cidr', 'dst_cidr', 'port_range', 'action']
            if not all(field in rule1 and field in rule2 for field in required):
                continue
            
            # Check if rules overlap in terms of traffic they match
            if (rule1['protocol'] == rule2['protocol'] and 
                cidr_overlaps(rule1['src_cidr'], rule2['src_cidr']) and
                cidr_overlaps(rule1['dst_cidr'], rule2['dst_cidr'])):
                
                try:
                    port1 = parse_port_range(rule1['port_range'])
                    port2 = parse_port_range(rule2['port_range'])
                    
                    if port_ranges_overlap(port1, port2):
                        # Check for exact match (redundancy)
                        if (rule1['src_cidr'] == rule2['src_cidr'] and
                            rule1['dst_cidr'] == rule2['dst_cidr'] and
                            rule1['port_range'] == rule2['port_range'] and
                            rule1['action'] == rule2['action']):
                            issues.append({
                                'ruleId': rule2['id'],
                                'issue_type': 'redundancy',
                                'description': f'Redundant rule matches rule {rule1["id"]}',
                                'severity': 'warning'
                            })
                        
                        # Check for conflict (same conditions, different actions)
                        elif (rule1['src_cidr'] == rule2['src_cidr'] and
                              rule1['dst_cidr'] == rule2['dst_cidr'] and
                              rule1['port_range'] == rule2['port_range'] and
                              rule1['action'] != rule2['action']):
                            issues.append({
                                'ruleId': rule2['id'],
                                'issue_type': 'conflict',
                                'description': f'Conflicts with rule {rule1["id"]}',
                                'severity': 'critical'
                            })
                        
                        # Check for shadow (rule2 is more specific but will never be reached)
                        elif (cidr_contains(rule1['src_cidr'], rule2['src_cidr']) and
                              cidr_contains(rule1['dst_cidr'], rule2['dst_cidr'])):
                            # Rule1 is more general and higher priority, so rule2 is shadowed
                            issues.append({
                                'ruleId': rule2['id'],
                                'issue_type': 'shadow',
                                'description': f'Shadowed by higher priority rule {rule1["id"]}',
                                'severity': 'warning'
                            })
                except ValueError:
                    # Port range parsing failed, skip this comparison
                    continue
    
    return issues

def main():
    try:
        # Read from stdin
        input_data = sys.stdin.read().strip()
        rules = json.loads(input_data)
        
        all_issues = []
        
        # Validate each rule
        for rule in rules:
            issues = validate_rule(rule)
            all_issues.extend(issues)
        
        # Check for conflicts, redundancy, and shadows only if basic validation passes
        if not any(issue['severity'] == 'critical' for issue in all_issues):
            conflict_issues = check_conflicts_and_shadows(rules)
            all_issues.extend(conflict_issues)
        
        # Determine if valid
        is_valid = len(all_issues) == 0
        
        result = {
            'valid': is_valid,
            'issues': all_issues
        }
        
        print(json.dumps(result))
        
    except json.JSONDecodeError:
        result = {
            'valid': False,
            'issues': [{
                'ruleId': 'unknown',
                'issue_type': 'validation',
                'description': 'Invalid JSON format',
                'severity': 'critical'
            }]
        }
        print(json.dumps(result))
    except Exception as e:
        result = {
            'valid': False,
            'issues': [{
                'ruleId': 'unknown',
                'issue_type': 'validation',
                'description': f'Processing error: {str(e)}',
                'severity': 'critical'
            }]
        }
        print(json.dumps(result))

if __name__ == '__main__':
    main()