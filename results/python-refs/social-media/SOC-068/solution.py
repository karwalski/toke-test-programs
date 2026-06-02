import json
import sys
import re

def parse_mentions(content):
    # Find all @mentions in the content
    mention_pattern = r'@(\w+)'
    matches = re.findall(mention_pattern, content)
    
    # Create mentions list with mock user IDs
    mentions = []
    user_id_map = {'bob': 2, 'carol': 3}  # Mock user database
    
    for username in matches:
        if username in user_id_map:
            mentions.append({
                'username': username,
                'id': user_id_map[username]
            })
    
    return mentions

def main():
    # Read JSON from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract data
    action = input_data.get('action')
    token = input_data.get('token')
    post_id = input_data.get('post_id')
    content = input_data.get('content')
    
    # Parse mentions
    mentions = parse_mentions(content)
    
    # Create response
    response = {
        'comment_id': 3,
        'content': content,
        'mentions': mentions,
        'status': 'created'
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == '__main__':
    main()