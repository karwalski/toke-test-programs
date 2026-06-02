import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

class JSONRPCHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/rpc':
            self.send_error(404)
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            request = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400)
            return
        
        response = self.handle_jsonrpc(request)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_jsonrpc(self, request):
        if not isinstance(request, dict):
            return {"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": None}
        
        jsonrpc = request.get('jsonrpc')
        method = request.get('method')
        params = request.get('params')
        req_id = request.get('id')
        
        if jsonrpc != "2.0":
            return {"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": req_id}
        
        if method == "add":
            if isinstance(params, list) and len(params) == 2 and all(isinstance(p, (int, float)) for p in params):
                result = params[0] + params[1]
                return {"jsonrpc": "2.0", "result": result, "id": req_id}
        elif method == "subtract":
            if isinstance(params, list) and len(params) == 2 and all(isinstance(p, (int, float)) for p in params):
                result = params[0] - params[1]
                return {"jsonrpc": "2.0", "result": result, "id": req_id}
        elif method == "multiply":
            if isinstance(params, list) and len(params) == 2 and all(isinstance(p, (int, float)) for p in params):
                result = params[0] * params[1]
                return {"jsonrpc": "2.0", "result": result, "id": req_id}
        
        return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": req_id}
    
    def log_message(self, format, *args):
        pass

def run_server(port):
    server = HTTPServer(('', port), JSONRPCHandler)
    print(f"Listening on :{port}")
    
    # Run server in background thread for a short time to simulate startup
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Simulate server running briefly then exit
    time.sleep(0.1)
    server.shutdown()

port = int(input().strip())
run_server(port)