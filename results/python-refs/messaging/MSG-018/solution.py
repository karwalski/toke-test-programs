import sys

def matches_pattern(topic, pattern):
    topic_parts = topic.split('/')
    pattern_parts = pattern.split('/')
    
    # Handle # wildcard - must be at the end and matches everything after
    if '#' in pattern_parts:
        hash_index = pattern_parts.index('#')
        if hash_index != len(pattern_parts) - 1:
            return False
        # Check parts before #
        if hash_index > len(topic_parts):
            return False
        for i in range(hash_index):
            if pattern_parts[i] != '*' and pattern_parts[i] != topic_parts[i]:
                return False
        return True
    
    # No # wildcard - lengths must match exactly
    if len(topic_parts) != len(pattern_parts):
        return False
    
    # Check each part
    for i in range(len(topic_parts)):
        if pattern_parts[i] != '*' and pattern_parts[i] != topic_parts[i]:
            return False
    
    return True

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Parse subscriptions
n = int(lines[0])
subscriptions = []
for i in range(1, n + 1):
    subscriptions.append(lines[i])

# Parse messages (skip blank line at index n+1)
messages = []
for i in range(n + 2, len(lines)):
    if '|' in lines[i]:
        topic, message = lines[i].split('|', 1)
        messages.append((topic, message))

# Process each message
for topic, message in messages:
    print(f"{topic}:")
    for pattern in subscriptions:
        if matches_pattern(topic, pattern):
            print(f"  {pattern}")