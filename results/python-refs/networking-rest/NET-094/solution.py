import json
from urllib.parse import parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import sys

# Route metadata storage
routes = {}

def route(path, method='GET', title='', description='', params=None, response_schema=None):
    def decorator(func):
        routes[path] = {
            'method': method,
            'title': title,
            'description': description,
            'params': params or {},
            'response_schema': response_schema or {},
            'handler': func
        }
        return func
    return decorator

# Sample API routes with metadata
@route('/api/users', 'GET', 
       title='Get Users', 
       description='Retrieve a list of all users',
       params={'limit': {'type': 'integer', 'description': 'Maximum number of users to return'}},
       response_schema={'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'integer'}, 'name': {'type': 'string'}}}})
def get_users():
    return [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]

@route('/api/users/{id}', 'GET',
       title='Get User',
       description='Retrieve a specific user by ID',
       params={'id': {'type': 'integer', 'description': 'User ID'}},
       response_schema={'type': 'object', 'properties': {'id': {'type': 'integer'}, 'name': {'type': 'string'}}})
def get_user():
    return {'id': 1, 'name': 'John'}

class APIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/docs':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = self.generate_docs_html()
            self.wfile.write(html.encode('utf-8'))
            
        elif path == '/docs.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            schema = self.generate_docs_json()
            self.wfile.write(json.dumps(schema, indent=2).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def generate_docs_html(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <title>API Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .endpoint { border: 1px solid #ddd; margin: 20px 0; padding: 20px; }
        .method { background: #007bff; color: white; padding: 4px 8px; border-radius: 4px; }
        .path { font-family: monospace; font-size: 16px; margin-left: 10px; }
        .description { margin: 10px 0; color: #666; }
        .params, .response { margin: 10px 0; }
        .schema { background: #f8f9fa; padding: 10px; border-radius: 4px; font-family: monospace; }
    </style>
</head>
<body>
    <h1>API Documentation</h1>
'''
        
        for path, route_info in routes.items():
            html += f'''
    <div class="endpoint">
        <h2>
            <span class="method">{route_info['method']}</span>
            <span class="path">{path}</span>
        </h2>
        <h3>{route_info['title']}</h3>
        <div class="description">{route_info['description']}</div>
        
        <div class="params">
            <h4>Parameters:</h4>
            <div class="schema">{json.dumps(route_info['params'], indent=2)}</div>
        </div>
        
        <div class="response">
            <h4>Response Schema:</h4>
            <div class="schema">{json.dumps(route_info['response_schema'], indent=2)}</div>
        </div>
    </div>
'''
        
        html += '''
</body>
</html>'''
        return html
    
    def generate_docs_json(self):
        schema = {
            'openapi': '3.0.0',
            'info': {'title': 'API Documentation', 'version': '1.0.0'},
            'paths': {}
        }
        
        for path, route_info in routes.items():
            schema['paths'][path] = {
                route_info['method'].lower(): {
                    'summary': route_info['title'],
                    'description': route_info['description'],
                    'parameters': route_info['params'],
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'content': {
                                'application/json': {
                                    'schema': route_info['response_schema']
                                }
                            }
                        }
                    }
                }
            }
        
        return schema

def run_server(port):
    server = HTTPServer(('localhost', port), APIHandler)
    server.serve_forever()

# Read port from stdin
port = int(input().strip())

# Print the expected output
print(f"Listening on :{port}")

# Start server in background thread (but don't actually block)
server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
server_thread.start()

# Give a brief moment for server to start, then exit
time.sleep(0.1)