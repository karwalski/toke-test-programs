import json
import hashlib
import secrets
import base64
from urllib.parse import parse_qs, urlparse
import sys

def generate_session_id():
    return secrets.token_urlsafe(32)

def create_cookie_header(session_id):
    return f"session_id={session_id}; Path=/; HttpOnly"

def parse_cookie_header(cookie_header):
    if not cookie_header:
        return {}
    cookies = {}
    for cookie in cookie_header.split(';'):
        if '=' in cookie:
            key, value = cookie.strip().split('=', 1)
            cookies[key] = value
    return cookies

class HTTPServer:
    def __init__(self):
        self.sessions = {}
    
    def handle_post_login(self, headers, body):
        session_id = generate_session_id()
        self.sessions[session_id] = {"authenticated": True}
        
        response = {
            "status": "success",
            "message": "Login successful"
        }
        
        return {
            "status_code": 200,
            "headers": {
                "Content-Type": "application/json",
                "Set-Cookie": create_cookie_header(session_id)
            },
            "body": json.dumps(response)
        }
    
    def handle_get_profile(self, headers, body):
        cookie_header = headers.get("Cookie", "")
        cookies = parse_cookie_header(cookie_header)
        session_id = cookies.get("session_id")
        
        if not session_id or session_id not in self.sessions:
            response = {
                "status": "error",
                "message": "Unauthorized"
            }
            return {
                "status_code": 401,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(response)
            }
        
        response = {
            "status": "success",
            "message": "Profile data",
            "data": {"user": "authenticated_user"}
        }
        
        return {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response)
        }
    
    def handle_post_logout(self, headers, body):
        cookie_header = headers.get("Cookie", "")
        cookies = parse_cookie_header(cookie_header)
        session_id = cookies.get("session_id")
        
        if session_id and session_id in self.sessions:
            del self.sessions[session_id]
        
        response = {
            "status": "success",
            "message": "Logout successful"
        }
        
        return {
            "status_code": 200,
            "headers": {
                "Content-Type": "application/json",
                "Set-Cookie": "session_id=; Path=/; HttpOnly; Expires=Thu, 01 Jan 1970 00:00:00 GMT"
            },
            "body": json.dumps(response)
        }
    
    def handle_request(self, method, path, headers, body):
        if method == "POST" and path == "/login":
            return self.handle_post_login(headers, body)
        elif method == "GET" and path == "/profile":
            return self.handle_get_profile(headers, body)
        elif method == "POST" and path == "/logout":
            return self.handle_post_logout(headers, body)
        else:
            response = {
                "status": "error",
                "message": "Not Found"
            }
            return {
                "status_code": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(response)
            }

def main():
    port = input().strip()
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()