import socket
import sys

def resolve_hostname(hostname):
    a_records = []
    aaaa_records = []
    
    try:
        # Get A records (IPv4)
        result = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)
        for addr_info in result:
            ip = addr_info[4][0]
            if ip not in a_records:
                a_records.append(ip)
    except:
        pass
    
    try:
        # Get AAAA records (IPv6)
        result = socket.getaddrinfo(hostname, None, socket.AF_INET6, socket.SOCK_STREAM)
        for addr_info in result:
            ip = addr_info[4][0]
            if ip not in aaaa_records:
                aaaa_records.append(ip)
    except:
        pass
    
    return a_records, aaaa_records

def reverse_lookup(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        return ip

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(' ', 1)
        if len(parts) != 2:
            continue
            
        command, target = parts
        
        if command == "forward":
            a_records, aaaa_records = resolve_hostname(target)
            
            output = f"{target}:"
            
            if a_records:
                output += f" A={','.join(a_records)}"
            
            if aaaa_records:
                output += f" AAAA={','.join(aaaa_records)}"
            
            print(output)
            
        elif command == "reverse":
            hostname = reverse_lookup(target)
            print(f"{target}: {hostname}")

if __name__ == "__main__":
    main()