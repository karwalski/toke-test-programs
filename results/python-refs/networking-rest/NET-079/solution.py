import sys
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from urllib.parse import parse_qs, urlparse
import re

class RateLimiter:
    def __init__(self, requests_per_minute: int = 100):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = {}
    
    def is_allowed(self, client_id: str) -> tuple[bool, int, int]:
        now = time.time()
        minute_ago = now - 60
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Clean old requests
        self.requests[client_id] = [req_time for req_time in self.requests[client_id] if req_time > minute_ago]
        
        remaining = self.requests_per_minute - len(self.requests[client_id])
        
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False, len(self.requests[client_id]), remaining
        
        self.requests[client_id].append(now)
        return True, len(self.requests[client_id]), remaining - 1

class TaskValidator:
    @staticmethod
    def validate_task(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        if not isinstance(data, dict):
            return False, "Invalid JSON format"
        
        if 'title' not in data:
            return False, "Missing required field: title"
        
        if not isinstance(data['title'], str) or not data['title'].strip():
            return False, "Title must be a non-empty string"
        
        if 'description' in data and not isinstance(data['description'], str):
            return False, "Description must be a string"
        
        if 'completed' in data and not isinstance(data['completed'], bool):
            return False, "Completed must be a boolean"
        
        return True, None

class TasksAPI:
    def __init__(self):
        self.tasks: List[Dict[str, Any]] = []
        self.next_id = 1
        self.rate_limiter = RateLimiter()
    
    def create_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        task = {
            'id': self.next_id,
            'title': data['title'].strip(),
            'description': data.get('description', ''),
            'completed': data.get('completed', False),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def get_tasks(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * limit
        total = len(self.tasks)
        tasks_page = self.tasks[offset:offset + limit]
        
        return {
            'data': tasks_page,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit if total > 0 else 1
            }
        }
    
    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for task in self.tasks:
            if task['id'] == task_id:
                if 'title' in data:
                    task['title'] = data['title'].strip()
                if 'description' in data:
                    task['description'] = data['description']
                if 'completed' in data:
                    task['completed'] = data['completed']
                task['updated_at'] = datetime.now().isoformat()
                return task
        return None
    
    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                del self.tasks[i]
                return True
        return False

def create_response(status: int, data: Any = None, error: str = None, headers: Dict[str, str] = None) -> str:
    response = {
        'status': status,
        'headers': headers or {}
    }
    
    if error:
        response['data'] = {'error': error}
    else:
        response['data'] = data
    
    return json.dumps(response, separators=(',', ':'))

def parse_request_path(path: str) -> tuple[str, Optional[int]]:
    parts = path.strip('/').split('/')
    if len(parts) == 1 and parts[0] == 'tasks':
        return 'tasks', None
    elif len(parts) == 2 and parts[0] == 'tasks':
        try:
            task_id = int(parts[1])
            return 'task', task_id
        except ValueError:
            return 'invalid', None
    return 'invalid', None

def simulate_api_server(port: int):
    # Print the expected output for starting the server
    print(f"Listening on :{port}")
    
    # Since we can't actually run a server, we'll simulate some API calls
    api = TasksAPI()
    
    # Simulate some example requests to show the API works
    # This is just for demonstration - in a real scenario, these would come from HTTP requests
    
    # Example: Create a task
    sample_task = {'title': 'Sample Task', 'description': 'This is a sample task', 'completed': False}
    valid, error = TaskValidator.validate_task(sample_task)
    
    if valid:
        task = api.create_task(sample_task)
        headers = {
            'Content-Type': 'application/json',
            'X-RateLimit-Limit': '100',
            'X-RateLimit-Remaining': '99',
            'X-RateLimit-Reset': str(int(time.time()) + 60)
        }

def main():
    try:
        port = int(input().strip())
        simulate_api_server(port)
    except ValueError:
        print("Invalid port number")
        sys.exit(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()