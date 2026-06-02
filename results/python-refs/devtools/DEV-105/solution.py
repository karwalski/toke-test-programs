import sys

def convert_path(path, target_format):
    # First, normalize the path by replacing all separators with forward slashes
    normalized = path.replace('\\', '/')
    
    if target_format == 'unix':
        # For Unix format, keep forward slashes
        # Remove drive letters (C:, D:, etc.)
        if len(normalized) >= 2 and normalized[1] == ':':
            normalized = normalized[2:]
        return normalized
    
    elif target_format == 'windows':
        # For Windows format, use backslashes
        # Add C: drive if not present and path is absolute
        if normalized.startswith('/') and not (len(normalized) >= 3 and normalized[2] == ':'):
            normalized = 'C:' + normalized
        return normalized.replace('/', '\\')
    
    elif target_format == 'url':
        # For URL format, use forward slashes and encode spaces
        # Remove drive letters and ensure it starts with /
        if len(normalized) >= 2 and normalized[1] == ':':
            normalized = normalized[2:]
        if not normalized.startswith('/'):
            normalized = '/' + normalized
        # URL encode spaces and other special characters
        normalized = normalized.replace(' ', '%20')
        return normalized
    
    return path

# Read input
lines = sys.stdin.read().strip().split('\n')
target_format = lines[0]
paths = lines[1:]

# Convert and output each path
for path in paths:
    converted = convert_path(path, target_format)
    print(converted)