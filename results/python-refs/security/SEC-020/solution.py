import sys
import json
import re

def parse_rule(rule_line):
    # Parse a Snort-like rule
    # Format: action protocol src_ip src_port -> dst_ip dst_port (options)
    
    # Basic regex to parse rule components
    pattern = r'(\w+)\s+(\w+)\s+(\S+)\s+(\S+)\s+->\s+(\S+)\s+(\S+)\s+\((.*)\)'
    match = re.match(pattern, rule_line.strip())
    
    if not match:
        return None
    
    action, protocol, src_ip, src_port, dst_ip, dst_port, options = match.groups()
    
    # Parse options for msg
    msg = ""
    msg_match = re.search(r'msg:"([^"]*)"', options)
    if msg_match:
        msg = msg_match.group(1)
    
    return {
        'action': action,
        'protocol': protocol,
        'src_ip': src_ip,
        'src_port': src_port,
        'dst_ip': dst_ip,
        'dst_port': dst_port,
        'msg': msg
    }

def matches_rule(packet, rule):
    # Check if packet matches rule criteria
    
    # Check protocol
    if rule['protocol'] != 'any' and packet.get('proto') != rule['protocol']:
        return False
    
    # Check destination port
    if rule['dst_port'] != 'any':
        try:
            rule_port = int(rule['dst_port'])
            packet_port = packet.get('dport')
            if packet_port != rule_port:
                return False
        except ValueError:
            return False
    
    # Check source IP (any means match all)
    if rule['src_ip'] != 'any':
        if packet.get('src') != rule['src_ip']:
            return False
    
    # Check destination IP (any means match all)
    if rule['dst_ip'] != 'any':
        if packet.get('dst') != rule['dst_ip']:
            return False
    
    # Check source port
    if rule['src_port'] != 'any':
        try:
            rule_sport = int(rule['src_port'])
            packet_sport = packet.get('sport')
            if packet_sport != rule_sport:
                return False
        except ValueError:
            return False
    
    return True

def main():
    # Read rules from stdin
    rules = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            rule = parse_rule(line)
            if rule:
                rules.append(rule)
        except EOFError:
            break
    
    # Read packet summaries and check against rules
    while True:
        try:
            line = input().strip()
            if not line:
                continue
            
            try:
                packet = json.loads(line)
                
                # Check packet against all rules
                for rule in rules:
                    if matches_rule(packet, rule):
                        print(rule['msg'])
                        
            except json.JSONDecodeError:
                continue
                
        except EOFError:
            break

if __name__ == "__main__":
    main()