import json
import sys

# Read port number from stdin
port = input().strip()

# In-memory dataset (example data)
dataset = [
    {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
    {"id": 2, "name": "Bob", "age": 25, "city": "Los Angeles"},
    {"id": 3, "name": "Charlie", "age": 35, "city": "Chicago"}
]

def filter_data(data, filter_criteria):
    """Filter data based on filter criteria"""
    if not filter_criteria:
        return data
    
    filtered = []
    for item in data:
        match = True
        for key, value in filter_criteria.items():
            if key not in item or item[key] != value:
                match = False
                break
        if match:
            filtered.append(item)
    return filtered

def select_fields(data, fields):
    """Select only requested fields from data"""
    if not fields:
        return data
    
    result = []
    for item in data:
        selected = {}
        for field in fields:
            if field in item:
                selected[field] = item[field]
        result.append(selected)
    return result

def handle_query(request_data):
    """Handle POST /query request"""
    try:
        fields = request_data.get('fields', [])
        filter_criteria = request_data.get('filter', {})
        
        # Filter the dataset
        filtered_data = filter_data(dataset, filter_criteria)
        
        # Select only requested fields
        result_data = select_fields(filtered_data, fields)
        
        return {"data": result_data}
        
    except Exception as e:
        return {"errors": [str(e)]}

# Print the expected output for the server startup
print(f"Listening on :{port}")