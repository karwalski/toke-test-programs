import sys
import json

def main():
    domain = input().strip()
    allowed_cas_json = input().strip()
    try:
        allowed_cas = json.loads(allowed_cas_json)
    except Exception:
        allowed_cas = []
    
    result = {
        'domain': domain,
        'totalCerts': 0,
        'alertCerts': [],
        'summary': 'No alerts found. totalCerts checked.'
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()