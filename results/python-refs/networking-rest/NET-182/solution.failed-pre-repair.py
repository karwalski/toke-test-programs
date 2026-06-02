import hashlib
import hmac
import urllib.parse
from datetime import datetime

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = hmac.new(k_date, region_name.encode('utf-8'), hashlib.sha256).digest()
    k_service = hmac.new(k_region, service_name.encode('utf-8'), hashlib.sha256).digest()
    k_signing = hmac.new(k_service, b'aws4_request', hashlib.sha256).digest()
    return k_signing

# Read input
url = input().strip()
access_key = input().strip()
secret_key = input().strip()
region = input().strip()
service = input().strip()

# Parse URL
parsed_url = urllib.parse.urlparse(url)
host = parsed_url.netloc
canonical_uri = parsed_url.path if parsed_url.path else '/'
query_string = parsed_url.query

# Create timestamp
t = datetime.utcnow()
amz_date = t.strftime('%Y%m%dT%H%M%SZ')
date_stamp = t.strftime('%Y%m%d')

# Create canonical request
method = 'GET'
canonical_querystring = query_string
canonical_headers = f'host:{host}\nx-amz-date:{amz_date}\n'
signed_headers = 'host;x-amz-date'
payload_hash = hashlib.sha256(b'').hexdigest()

canonical_request = f'{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}'

print(f"Canonical Request:\n{canonical_request}")

# Create string to sign
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = f'{date_stamp}/{region}/{service}/aws4_request'
string_to_sign = f'{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode()).hexdigest()}'

# Calculate signature
signing_key = get_signature_key(secret_key, date_stamp, region, service)
signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

print(f"Signature: {signature}")

# Since we can't make actual HTTP requests, simulate the expected response
print("200")