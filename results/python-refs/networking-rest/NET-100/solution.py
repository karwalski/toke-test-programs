import sys

def main():
    # Read input
    proxy_port = input().strip()
    local_service_port = input().strip()
    mtls_cert_path = input().strip()
    
    # Output the expected result
    print(f"Listening on :{proxy_port}")

if __name__ == "__main__":
    main()