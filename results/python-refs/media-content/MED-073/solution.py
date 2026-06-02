import sys

def generate_breadcrumb(path):
    # Remove leading slash and split into parts
    parts = path.strip('/').split('/')
    
    # Start with Home link
    breadcrumb = '<nav><a href="/">Home</a>'
    
    # Build cumulative path and add links
    current_path = ''
    for i, part in enumerate(parts):
        current_path += '/' + part
        
        if i == len(parts) - 1:
            # Last part is not a link
            breadcrumb += ' / ' + part
        else:
            # Intermediate parts are links
            breadcrumb += ' / <a href="' + current_path + '">' + part + '</a>'
    
    breadcrumb += '</nav>'
    return breadcrumb

# Read from stdin
path = input().strip()
result = generate_breadcrumb(path)
print(result)