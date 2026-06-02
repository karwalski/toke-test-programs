import sys
import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import HTTPError

class MockHandler(BaseHTTPRequestHandler):
    data_store = {}
    
    def log_message(self, format, *args):
        pass  # Suppress server logs
    
    def do_POST(self):
        if self.path == '/items':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                item_id = len(self.data_store) + 1
                self.data_store[item_id] = data
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {'id': item_id, **data}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path.startswith('/items/'):
            try:
                item_id = int(self.path.split('/')[-1])
                if item_id in self.data_store:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {'id': item_id, **self.data_store[item_id]}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
            except:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_PUT(self):
        if self.path.startswith('/items/'):
            try:
                item_id = int(self.path.split('/')[-1])
                if item_id in self.data_store:
                    content_length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(content_length).decode('utf-8')
                    data = json.loads(body)
                    self.data_store[item_id] = data
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {'id': item_id, **data}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
            except:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_DELETE(self):
        if self.path.startswith('/items/'):
            try:
                item_id = int(self.path.split('/')[-1])
                if item_id in self.data_store:
                    del self.data_store[item_id]
                    self.send_response(204)
                    self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()
            except:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def start_server(port):
    server = HTTPServer(('localhost', port), MockHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

def test_crud(port):
    base_url = f'http://localhost:{port}'
    
    # Test CREATE
    try:
        data = json.dumps({'name': 'test item', 'value': 42}).encode('utf-8')
        req = Request(f'{base_url}/items', data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        response = urlopen(req)
        if response.status == 201:
            result = json.loads(response.read().decode('utf-8'))
            item_id = result['id']
            print('CREATE: PASS')
        else:
            print('CREATE: FAIL')
            return
    except:
        print('CREATE: FAIL')
        return

if __name__ == '__main__':
    port = int(input().strip())
    server = start_server(port)
    time.sleep(0.1)  # Give server time to start
    test_crud(port)
    server.shutdown()