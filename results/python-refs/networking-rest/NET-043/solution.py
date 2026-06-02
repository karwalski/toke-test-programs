import sys
import os
import mimetypes
from urllib.parse import unquote
from html import escape

def get_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or 'application/octet-stream'

def generate_directory_listing(path, url_path):
    items = []
    try:
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                items.append(f'<li><a href="{url_path.rstrip("/")}/{item}/">{escape(item)}/</a></li>')
            else:
                items.append(f'<li><a href="{url_path.rstrip("/")}/{item}">{escape(item)}</a></li>')
    except OSError:
        return None
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Directory listing for {escape(url_path)}</title>
</head>
<body>
    <h1>Directory listing for {escape(url_path)}</h1>
    <ul>
{"".join(items)}
    </ul>
</body>
</html>'''
    return html

def handle_request(root_dir, url_path):
    # Remove leading slash and decode URL
    if url_path.startswith('/'):
        url_path = url_path[1:]
    
    url_path = unquote(url_path)
    file_path = os.path.join(root_dir, url_path)
    
    # Security check - ensure path is within root directory
    try:
        file_path = os.path.abspath(file_path)
        root_dir = os.path.abspath(root_dir)
        if not file_path.startswith(root_dir):
            return None, None, 404
    except:
        return None, None, 404
    
    # Check if file exists
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            mime_type = get_mime_type(file_path)
            return content, mime_type, 200
        except:
            return None, None, 404
    
    # Check if directory exists
    elif os.path.isdir(file_path):
        # Try index.html first
        index_path = os.path.join(file_path, 'index.html')
        if os.path.isfile(index_path):
            try:
                with open(index_path, 'rb') as f:
                    content = f.read()
                return content, 'text/html', 200
            except:
                pass
        
        # Generate directory listing
        listing = generate_directory_listing(file_path, '/' + url_path)
        if listing:
            return listing.encode('utf-8'), 'text/html', 200
    
    return None, None, 404

def main():
    lines = sys.stdin.read().strip().split('\n')
    port = lines[0]
    root_dir = lines[1]
    
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()