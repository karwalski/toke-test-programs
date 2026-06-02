import json
import ipaddress
import sys

def ip_in_cidr(ip, cidr):
    """Check if an IP address is in a CIDR block"""
    try:
        return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr, strict=False)
    except:
        return False

def find_segment_for_ip(ip, segments):
    """Find which segment an IP belongs to"""
    for segment in segments:
        if ip_in_cidr(ip, segment['cidr']):
            return segment
    return None

def check_connectivity(src_ip, dst_ip, segments):
    """Check if connectivity is allowed between src and dst IPs"""
    # Find source segment
    src_segment = find_segment_for_ip(src_ip, segments)
    if not src_segment:
        return "deny"
    
    # Check if destination is in any allowed outbound CIDR
    for allowed_cidr in src_segment.get('allowed_outbound', []):
        if ip_in_cidr(dst_ip, allowed_cidr):
            return "allow"
    
    return "deny"

def main():
    # Read JSON from stdin
    input_data = json.load(sys.stdin)
    
    segments = input_data['segments']
    test_pairs = input_data['test_pairs']
    
    results = []
    
    # Process each test pair
    for test_pair in test_pairs:
        src = test_pair['src']
        dst = test_pair['dst']
        expected = test_pair['expected']
        
        actual = check_connectivity(src, dst, segments)
        
        if actual == expected:
            results.append("PASS")
        else:
            results.append("FAIL")
    
    # Output results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()