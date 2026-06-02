import urllib.request
import urllib.error
import sys

def probe_file(base_url, path):
    """Probe a single file path and return result"""
    if not base_url.endswith('/'):
        base_url += '/'
    
    full_url = base_url + path
    
    try:
        response = urllib.request.urlopen(full_url)
        status = response.getcode()
        content = response.read(100).decode('utf-8', errors='ignore')
        content_preview = content.replace('\n', ' ').replace('\r', ' ')[:50]
        if len(content) > 50:
            content_preview += '...'
        return f"EXPOSED: {path} ({status}, {content_preview})"
    except urllib.error.HTTPError as e:
        return f"NOT FOUND: {path}"
    except Exception as e:
        return f"NOT FOUND: {path}"

def main():
    # Read base URL from stdin
    base_url = input().strip()
    
    # List of sensitive files to probe
    sensitive_files = [
        '.env',
        '.git/config',
        '.htpasswd',
        'web.config',
        'phpinfo.php',
        'backup.sql'
    ]
    
    # Probe each file
    results = []
    exposed_count = 0
    
    for file_path in sensitive_files:
        result = probe_file(base_url, file_path)
        results.append(result)
        if result.startswith("EXPOSED:"):
            exposed_count += 1
    
    # Print summary
    print("Summary:")

if __name__ == "__main__":
    main()