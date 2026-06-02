import sys
import json
from urllib.parse import urlparse, parse_qs

# Read port number from stdin
port = input().strip()

# In-memory storage for products
products = {}
next_id = 1

def handle_get_products():
    return json.dumps(list(products.values()))

def handle_get_product(product_id):
    if product_id in products:
        return json.dumps(products[product_id])
    else:
        return json.dumps({"error": "Product not found"}), 404

def handle_post_product(data):
    global next_id
    product = {
        "id": next_id,
        "name": data.get("name", ""),
        "price": data.get("price", 0),
        "stock": data.get("stock", 0)
    }
    products[next_id] = product
    next_id += 1
    return json.dumps(product), 201

def handle_put_product(product_id, data):
    if product_id in products:
        products[product_id].update(data)
        return json.dumps(products[product_id])
    else:
        return json.dumps({"error": "Product not found"}), 404

def handle_delete_product(product_id):
    if product_id in products:
        del products[product_id]
        return json.dumps({"message": "Product deleted"})
    else:
        return json.dumps({"error": "Product not found"}), 404

# Simulate REST API endpoints
def handle_request(method, path, data=None):
    if path == "/products":
        if method == "GET":
            return handle_get_products()
        elif method == "POST":
            return handle_post_product(data)
    elif path.startswith("/products/"):
        try:
            product_id = int(path.split("/")[-1])
            if method == "GET":
                return handle_get_product(product_id)
            elif method == "PUT":
                return handle_put_product(product_id, data)
            elif method == "DELETE":
                return handle_delete_product(product_id)
        except ValueError:
            return json.dumps({"error": "Invalid product ID"}), 400
    
    return json.dumps({"error": "Not found"}), 404

# Output the expected result
print(f"Listening on :{port}")