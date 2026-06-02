import sys
import time
from collections import defaultdict

class TokenBucket:
    def __init__(self, tokens_per_second):
        self.tokens_per_second = tokens_per_second
        self.tokens = tokens_per_second
        self.last_refill = time.time()
    
    def consume(self):
        now = time.time()
        # Refill tokens based on time elapsed
        elapsed = now - self.last_refill
        self.tokens = min(self.tokens_per_second, self.tokens + elapsed * self.tokens_per_second)
        self.last_refill = now
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
    
    def get_reset_time(self):
        # Time until next token is available
        if self.tokens >= 1:
            return 0
        tokens_needed = 1 - self.tokens
        return int(tokens_needed / self.tokens_per_second) + 1

# Read input from stdin
lines = sys.stdin.read().strip().split('\n')
port = lines[0].strip()
buckets = {}

for i in range(1, len(lines)):
    line = lines[i].strip()
    if not line:
        break
    parts = line.split()
    api_key = parts[0]
    tokens_per_second = int(parts[1])
    buckets[api_key] = TokenBucket(tokens_per_second)

# Print expected output
print(f"Listening on :{port}")