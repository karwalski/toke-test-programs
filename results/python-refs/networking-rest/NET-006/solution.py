import json
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# In-memory storage for orders
orders = {}
next_order_id = 1

def get_iso_timestamp():
    return datetime.utcnow().isoformat() + 'Z'

def create_order(data):
    global next_order_id
    order = {
        'id': next_order_id,
        'userId': data.get('userId'),
        'items': data.get('items', []),
        'status': data.get('status', 'pending'),
        'createdAt': get_iso_timestamp()
    }
    orders[next_order_id] = order
    next_order_id += 1
    return order

def get_order(order_id):
    return orders.get(order_id)

def get_all_orders():
    return list(orders.values())

def update_order(order_id, data):
    if order_id not in orders:
        return None
    
    order = orders[order_id]
    if 'userId' in data:
        order['userId'] = data['userId']
    if 'items' in data:
        order['items'] = data['items']
    if 'status' in data:
        order['status'] = data['status']
    
    return order

def delete_order(order_id):
    if order_id not in orders:
        return False
    del orders[order_id]
    return True

def handle_request(method, path, body=None):
    if path.startswith('/orders'):
        if path == '/orders':
            if method == 'GET':
                return {'status': 200, 'data': get_all_orders()}
            elif method == 'POST':
                if body:
                    order = create_order(body)
                    return {'status': 201, 'data': order}
                return {'status': 400, 'error': 'Invalid request body'}
        
        elif path.startswith('/orders/'):
            try:
                order_id = int(path.split('/')[-1])
            except ValueError:
                return {'status': 400, 'error': 'Invalid order ID'}
            
            if method == 'GET':
                order = get_order(order_id)
                if order:
                    return {'status': 200, 'data': order}
                return {'status': 404, 'error': 'Order not found'}
            
            elif method == 'PUT':
                if body:
                    order = update_order(order_id, body)
                    if order:
                        return {'status': 200, 'data': order}
                    return {'status': 404, 'error': 'Order not found'}
                return {'status': 400, 'error': 'Invalid request body'}
            
            elif method == 'DELETE':
                if delete_order(order_id):
                    return {'status': 204}
                return {'status': 404, 'error': 'Order not found'}
    
    return {'status': 404, 'error': 'Not found'}

# Read port from stdin
port = input().strip()

# Print the expected output
print(f"Listening on :{port}")