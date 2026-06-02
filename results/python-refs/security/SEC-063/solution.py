import json
import urllib.request
import urllib.parse
import sys

def fetch_openapi_spec(base_url):
    """Fetch OpenAPI/Swagger specification from the API"""
    openapi_urls = ['/openapi.json', '/swagger.json']
    
    for endpoint in openapi_urls:
        try:
            url = urllib.parse.urljoin(base_url, endpoint)
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode())
        except:
            continue
    
    return None

def identify_sensitive_fields(schema_data):
    """Identify sensitive fields in schema definitions"""
    sensitive_keywords = [
        'password', 'token', 'secret', 'key', 'credential',
        'ssn', 'social', 'credit', 'card', 'cvv', 'pin',
        'email', 'phone', 'address', 'birth', 'salary'
    ]
    
    sensitive_fields = []
    
    def scan_properties(properties):
        fields = []
        if isinstance(properties, dict):
            for field_name, field_def in properties.items():
                field_lower = field_name.lower()
                if any(keyword in field_lower for keyword in sensitive_keywords):
                    fields.append(field_name)
                
                # Check nested properties
                if isinstance(field_def, dict):
                    if 'properties' in field_def:
                        fields.extend(scan_properties(field_def['properties']))
                    elif 'items' in field_def and isinstance(field_def['items'], dict) and 'properties' in field_def['items']:
                        fields.extend(scan_properties(field_def['items']['properties']))
        
        return fields
    
    if isinstance(schema_data, dict):
        if 'properties' in schema_data:
            sensitive_fields.extend(scan_properties(schema_data['properties']))
    
    return sensitive_fields

def check_auth_required(path_data):
    """Check if authentication is required for an endpoint"""
    for method_data in path_data.values():
        if isinstance(method_data, dict):
            # Check for security requirements
            if 'security' in method_data and method_data['security']:
                return True
            
            # Check for authorization parameters
            if 'parameters' in method_data:
                for param in method_data['parameters']:
                    if isinstance(param, dict):
                        param_name = param.get('name', '').lower()
                        if 'auth' in param_name or 'token' in param_name or 'key' in param_name:
                            return True
    
    return False

def calculate_risk_score(methods, auth_required, sensitive_fields):
    """Calculate risk score based on endpoint characteristics"""
    score = 0
    
    # Method-based scoring
    method_scores = {'GET': 1, 'POST': 3, 'PUT': 3, 'PATCH': 3, 'DELETE': 4}
    for method in methods:
        score += method_scores.get(method.upper(), 2)
    
    # Authentication scoring
    if not auth_required:
        score += 5
    
    # Sensitive data scoring
    score += len(sensitive_fields) * 2
    
    return min(score, 10)  # Cap at 10

def analyze_openapi_spec(spec):
    """Analyze OpenAPI specification and extract endpoint information"""
    if not spec or 'paths' not in spec:
        return []
    
    endpoints = []
    schemas = spec.get('components', {}).get('schemas', {})
    
    for path, path_data in spec['paths'].items():
        if not isinstance(path_data, dict):
            continue
            
        methods = []
        sensitive_fields = set()
        
        # Extract HTTP methods
        http_methods = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
        for method in http_methods:
            if method in path_data:
                methods.append(method.upper())
                
                # Analyze responses for sensitive data
                method_data = path_data[method]
                if 'responses' in method_data:
                    for response_code, response_data in method_data['responses'].items():
                        if isinstance(response_data, dict) and 'content' in response_data:
                            for content_type, content_data in response_data['content'].items():
                                if 'schema' in content_data:
                                    schema = content_data['schema']
                                    if '$ref' in schema:
                                        # Reference to component schema
                                        ref_name = schema['$ref'].split('/')[-1]
                                        if ref_name in schemas:
                                            sensitive_fields.update(identify_sensitive_fields(schemas[ref_name]))
                                    else:
                                        sensitive_fields.update(identify_sensitive_fields(schema))
        
        auth_required = check_auth_required(path_data)
        sensitive_fields_list = sorted(list(sensitive_fields))
        risk_score = calculate_risk_score(methods, auth_required, sensitive_fields_list)
        
        endpoints.append({
            'path': path,
            'methods': methods,
            'authRequired': auth_required,
            'sensitiveFields': sensitive_fields_list,
            'riskScore': risk_score
        })
    
    return endpoints

def generate_summary(endpoints):
    """Generate summary statistics"""
    total_endpoints = len(endpoints)
    high_risk = len([e for e in endpoints if e['riskScore'] >= 7])
    unauthenticated = len([e for e in endpoints if not e['authRequired']])
    with_sensitive_data = len([e for e in endpoints if e['sensitiveFields']])
    
    return {
        'totalEndpoints': total_endpoints,
        'highRiskEndpoints': high_risk,
        'unauthenticatedEndpoints': unauthenticated,
        'endpointsWithSensitiveData': with_sensitive_data
    }

def main():
    # Read base URL from stdin
    base_url = input().strip()
    
    # Fetch and analyze OpenAPI specification
    spec = fetch_openapi_spec(base_url)
    endpoints = analyze_openapi_spec(spec)
    
    print("endpoints")

if __name__ == '__main__':
    main()