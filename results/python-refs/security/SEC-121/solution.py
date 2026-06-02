import urllib.request
import urllib.parse
import sys

def test_ssrf(base_url, metadata_url):
    try:
        # Replace {URL} placeholder with the metadata URL
        test_url = base_url.replace("{URL}", urllib.parse.quote(metadata_url, safe=''))
        
        # Make request with short timeout
        req = urllib.request.Request(test_url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8', errors='ignore')
            # Check if response contains metadata-like content
            if len(content) > 10 and ('ami-' in content or 'instance' in content.lower() or 
                                     'metadata' in content.lower() or 'token' in content.lower() or
                                     'subscription' in content.lower()):
                return "ACCESSIBLE"
            else:
                return "BLOCKED"
    except:
        return "BLOCKED"

# Read input URL
input_url = input().strip()

# Metadata endpoints to test
endpoints = [
    ("AWS", "http://169.254.169.254/latest/meta-data/"),
    ("GCP", "http://metadata.google.internal/computeMetadata/v1/"),
    ("Azure", "http://169.254.169.254/metadata/instance?api-version=2021-02-01")
]

print("Testing")
any_accessible = False

for service, endpoint in endpoints:
    result = test_ssrf(input_url, endpoint)
    if result == "ACCESSIBLE":
        any_accessible = True

if any_accessible:
    print("CRITICAL")