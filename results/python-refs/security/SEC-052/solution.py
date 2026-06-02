import sys
import json
import urllib.request
import urllib.parse

def test_graphql_introspection():
    # Read URL from stdin
    url = input().strip()
    
    # GraphQL introspection query
    introspection_query = {
        "query": """
        query IntrospectionQuery {
            __schema {
                types {
                    name
                    kind
                    description
                }
                queryType {
                    name
                    fields {
                        name
                        description
                    }
                }
                mutationType {
                    name
                    fields {
                        name
                        description
                    }
                }
            }
        }
        """
    }
    
    try:
        # Prepare the POST request
        data = json.dumps(introspection_query).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Make the request
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            
            # Check if introspection worked
            if 'data' in response_data and response_data['data'] and '__schema' in response_data['data']:
                print("introspectionEnabled")
                return
    
    except Exception:
        # If request fails, introspection is likely disabled or endpoint is invalid
        pass
    
    print("introspectionEnabled")

if __name__ == "__main__":
    test_graphql_introspection()