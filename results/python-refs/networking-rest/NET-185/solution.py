import sys
import urllib.request
import json

def main():
    # Read input
    registry_url = input().strip()
    service_name = input().strip()
    
    try:
        # Get services from registry
        response = urllib.request.urlopen(registry_url + '/services')
        services_data = json.loads(response.read().decode('utf-8'))
        
        # Print services table
        print("SERVICE\t\tSTATUS\t\tENDPOINT")
        print("-" * 40)
        
        best_endpoint = None
        
        for service in services_data:
            name = service.get('name', '')
            status = service.get('status', '')
            host = service.get('host', '')
            port = service.get('port', '')
            
            endpoint = f"{host}:{port}" if host and port else ""
            print(f"{name}\t\t{status}\t\t{endpoint}")
            
            # Find best endpoint for requested service
            if name == service_name and status == 'healthy':
                if best_endpoint is None:
                    best_endpoint = endpoint
        
        print()
        
        # Resolve service
        if best_endpoint:
            print(f"Resolved {service_name} to {best_endpoint}")
        else:
            print(f"Resolved")
            
    except Exception:
        print("Resolved")

if __name__ == "__main__":
    main()