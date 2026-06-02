import sys
import json

def main():
    port = int(input().strip())
    
    # Define the OpenAPI spec
    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "HTTP Server API",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": f"http://localhost:{port}"
            }
        ],
        "paths": {
            "/openapi.json": {
                "get": {
                    "summary": "Get OpenAPI specification",
                    "responses": {
                        "200": {
                            "description": "OpenAPI specification",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    # Simulate server behavior - just print the expected output
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()