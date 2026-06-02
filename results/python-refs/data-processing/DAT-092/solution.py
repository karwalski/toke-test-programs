import sys
import json
from urllib.parse import urlparse, parse_qs, urlencode

for line in sys.stdin:
    url = line.strip()
    if not url:
        continue
    
    parsed = urlparse(url)
    
    result = {}
    
    # Add scheme (lowercase)
    if parsed.scheme:
        result["scheme"] = parsed.scheme.lower()
    
    # Add host (lowercase)
    if parsed.hostname:
        result["host"] = parsed.hostname.lower()
    
    # Add port if not default
    if parsed.port:
        result["port"] = parsed.port
    
    # Add path
    if parsed.path:
        result["path"] = parsed.path
    
    # Add query (sorted parameters)
    if parsed.query:
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        # Sort parameters and flatten single values
        sorted_params = []
        for key in sorted(query_params.keys()):
            for value in query_params[key]:
                sorted_params.append((key, value))
        result["query"] = urlencode(sorted_params)
    
    print(json.dumps(result, separators=(',', ':')))