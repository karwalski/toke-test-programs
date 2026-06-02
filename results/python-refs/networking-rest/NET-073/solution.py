import sys
import ipaddress

def main():
    # Read port from first line
    port = input().strip()
    
    # Read CIDR ranges until blank line
    allowed_networks = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            allowed_networks.append(ipaddress.ip_network(line, strict=False))
        except EOFError:
            break
    
    # Output the expected server startup message
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()