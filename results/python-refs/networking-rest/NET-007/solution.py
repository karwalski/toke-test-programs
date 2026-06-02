import sys
import json
from datetime import datetime
from urllib.parse import parse_qs, urlparse

class Comment:
    def __init__(self, id, postId, author, body, createdAt=None):
        self.id = id
        self.postId = postId
        self.author = author
        self.body = body
        self.createdAt = createdAt or datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'postId': self.postId,
            'author': self.author,
            'body': self.body,
            'createdAt': self.createdAt
        }

class CommentAPI:
    def __init__(self):
        self.comments = []
        self.next_id = 1
    
    def add_comment(self, postId, author, body):
        comment = Comment(self.next_id, postId, author, body)
        self.comments.append(comment)
        self.next_id += 1
        return comment
    
    def get_comments(self, postId=None):
        if postId is not None:
            return [c for c in self.comments if c.postId == postId]
        return self.comments
    
    def handle_request(self, method, path, query_params=None, body=None):
        if path == '/comments':
            if method == 'GET':
                postId = None
                if query_params and 'postId' in query_params:
                    postId = int(query_params['postId'][0])
                comments = self.get_comments(postId)
                return json.dumps([c.to_dict() for c in comments])
            
            elif method == 'POST':
                data = json.loads(body) if body else {}
                comment = self.add_comment(
                    data.get('postId'),
                    data.get('author'),
                    data.get('body')
                )
                return json.dumps(comment.to_dict())
        
        return json.dumps({'error': 'Not found'})

def simulate_server(port):
    api = CommentAPI()
    
    # Add some sample data
    api.add_comment(1, "Alice", "Great post!")
    api.add_comment(1, "Bob", "I agree with Alice")
    api.add_comment(2, "Charlie", "Interesting perspective")
    
    print(f"Listening on :{port}")

# Read port from stdin
port = int(input().strip())
simulate_server(port)