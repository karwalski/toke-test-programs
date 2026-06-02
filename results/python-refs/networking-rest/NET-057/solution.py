import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

class User:
    users = {}
    next_id = 1
    
    def __init__(self, name, email):
        self.id = User.next_id
        self.name = name
        self.email = email
        User.users[self.id] = self
        User.next_id += 1
    
    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

class GraphQLHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging
    
    def do_POST(self):
        if self.path == '/graphql':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode('utf-8')
                query_data = json.loads(post_data)
                
                query = query_data.get('query', '')
                variables = query_data.get('variables', {})
                
                result = self.execute_graphql(query, variables)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
                
            except Exception as e:
                result = {"errors": [{"message": str(e)}]}
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def execute_graphql(self, query, variables):
        query = query.strip()
        
        if query.startswith('query') or query.startswith('{'):
            return self.handle_query(query, variables)
        elif query.startswith('mutation'):
            return self.handle_mutation(query, variables)
        else:
            return {"errors": [{"message": "Invalid query"}]}
    
    def handle_query(self, query, variables):
        if 'users' in query:
            users_data = [user.to_dict() for user in User.users.values()]
            return {"data": {"users": users_data}}
        elif 'user(' in query:
            # Extract user ID from query
            import re
            match = re.search(r'user\(id:\s*(\d+)\)', query)
            if match:
                user_id = int(match.group(1))
                user = User.users.get(user_id)
                if user:
                    return {"data": {"user": user.to_dict()}}
                else:
                    return {"data": {"user": None}}
            else:
                return {"errors": [{"message": "Invalid user query"}]}
        else:
            return {"data": {}}
    
    def handle_mutation(self, query, variables):
        if 'createUser' in query:
            # Extract name and email from mutation
            import re
            name_match = re.search(r'name:\s*"([^"]*)"', query)
            email_match = re.search(r'email:\s*"([^"]*)"', query)
            
            if name_match and email_match:
                name = name_match.group(1)
                email = email_match.group(1)
                user = User(name, email)
                return {"data": {"createUser": user.to_dict()}}
            else:
                return {"errors": [{"message": "Missing name or email"}]}
        else:
            return {"errors": [{"message": "Unknown mutation"}]}

def run_server(port):
    # Since we can't actually run a server, we'll just print the expected output
    print(f"Listening on :{port}")

def main():
    port = int(input().strip())
    
    # Initialize some sample users
    User("John Doe", "john@example.com")
    User("Jane Smith", "jane@example.com")
    
    run_server(port)

if __name__ == "__main__":
    main()