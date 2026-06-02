import sys
import urllib.request
import urllib.error
import re

def find_api_keys(content):
    # Common API key patterns
    patterns = [
        (r'Bearer\s+[A-Za-z0-9\-_\.]+', 'Bearer token'),
        (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
        (r'[A-Za-z0-9+/]{40}', 'AWS Secret Key'),
        (r'sk-[A-Za-z0-9]{48}', 'OpenAI API Key'),
        (r'ghp_[A-Za-z0-9]{36}', 'GitHub Personal Access Token'),
        (r'ghs_[A-Za-z0-9]{36}', 'GitHub App Token'),
        (r'gho_[A-Za-z0-9]{36}', 'GitHub OAuth Token'),
        (r'AIza[0-9A-Za-z\-_]{35}', 'Google API Key'),
        (r'ya29\.[0-9A-Za-z\-_]+', 'Google OAuth Token'),
        (r'[0-9a-f]{32}', 'MD5 Hash/API Key'),
        (r'[0-9a-f]{64}', 'SHA256 Hash/API Key'),
        (r'xox[bpoa]-[0-9]{12}-[0-9]{12}-[0-9a-zA-Z]{24}', 'Slack Token'),
        (r'[A-Za-z0-9]{32}', 'Generic 32-char API Key'),
        (r'[A-Za-z0-9]{40}', 'Generic 40-char API Key'),
        (r'[A-Za-z0-9]{64}', 'Generic 64-char API Key')
    ]
    
    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        for pattern, pattern_type in patterns:
            if re.search(pattern, line):
                return f'FOUND: {pattern_type} at line {line_num} (redacted)'
    
    return 'CLEAN'

def scrape_url(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            return find_api_keys(content)
    except (urllib.error.URLError, urllib.error.HTTPError, UnicodeDecodeError, Exception):
        return 'CLEAN'

def main():
    for line in sys.stdin:
        url = line.strip()
        if url:
            result = scrape_url(url)
            print(result)

if __name__ == '__main__':
    main()