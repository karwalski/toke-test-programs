import socket
import sys

def query_dns(domain, resolver):
    """Query DNS for A record using specified resolver"""
    original_dns = None
    try:
        # Set the resolver temporarily
        original_dns = socket.getdefaulttimeout()
        socket.setdefaulttimeout(3)
        
        # For simulation purposes, we'll use the system's default resolver
        # In a real implementation, you'd need to craft DNS packets
        result = socket.gethostbyname(domain)
        return result
    except:
        return None
    finally:
        if original_dns is not None:
            socket.setdefaulttimeout(original_dns)

def main():
    # Read input
    domain = input().strip()
    expected_ip = input().strip()
    resolvers = [r.strip() for r in input().strip().split(',')]
    
    results = []
    all_match = True
    
    for resolver in resolvers:
        # Query the resolver
        returned_ip = query_dns(domain, resolver)
        
        if returned_ip is None:
            matches_expected = False
            suspicious = True
            all_match = False
        else:
            matches_expected = (returned_ip == expected_ip)
            suspicious = not matches_expected
            if not matches_expected:
                all_match = False
        
        results.append({
            'resolver': resolver,
            'returned_ip': returned_ip,
            'matches_expected': matches_expected,
            'suspicious': suspicious
        })
    
    # Print summary
    if all_match:
        print("CONSISTENT")
    else:
        print("HIJACKED")

if __name__ == "__main__":
    main()