import json
import sys
import os

def load_user_data():
    """Load user data from file or return empty dict if file doesn't exist"""
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    """Save user data to file"""
    with open('user_data.json', 'w') as f:
        json.dump(data, f)

def get_unread_count(last_seen_id):
    """Calculate unread count based on last seen ID"""
    # Simulate a feed with 62 total items
    total_items = 62
    return max(0, total_items - last_seen_id)

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    action = input_data.get('action')
    token = input_data.get('token')
    last_seen_id = input_data.get('last_seen_id')
    
    if action == 'sync_position':
        # Load existing user data
        user_data = load_user_data()
        
        # Update last seen position for this token
        if 'users' not in user_data:
            user_data['users'] = {}
        
        user_data['users'][token] = {
            'last_seen_id': last_seen_id
        }
        
        # Save updated data
        save_user_data(user_data)
        
        # Calculate unread count
        unread_count = get_unread_count(last_seen_id)
        
        # Create response
        response = {
            "last_seen_id": last_seen_id,
            "unread_count": unread_count,
            "status": "synced"
        }
        
        # Output response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()