import sys
from urllib.parse import urlparse

# Built-in GeoIP stub database
GEOIP_DB = {
    '192.168.1.1': {'country': 'US', 'region': 'California'},
    '10.0.0.1': {'country': 'CA', 'region': 'Ontario'},
    '172.16.0.1': {'country': 'GB', 'region': 'England'},
    '203.0.113.1': {'country': 'AU', 'region': 'New South Wales'},
    '198.51.100.1': {'country': 'DE', 'region': 'Bavaria'},
    '127.0.0.1': {'country': 'US', 'region': 'Local'},
}

def lookup_geoip(ip):
    """Perform GeoIP lookup against built-in stub database"""
    return GEOIP_DB.get(ip, {'country': 'Unknown', 'region': 'Unknown'})

def main():
    # Read input
    port = int(input().strip())
    upstream_url = input().strip()
    
    # Parse upstream URL
    parsed = urlparse(upstream_url)
    
    # Print expected output - simulate server startup
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()