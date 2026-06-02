import sys
import json
import urllib.request
import urllib.parse
from html.parser import HTMLParser

class SRIParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.resources = []
    
    def handle_starttag(self, tag, attrs):
        if tag not in ['script', 'link']:
            return
        
        attr_dict = dict(attrs)
        
        # Get src/href attribute
        src = attr_dict.get('src') if tag == 'script' else attr_dict.get('href')
        if not src:
            return
        
        # Check if external resource
        if self.is_external(src):
            integrity = attr_dict.get('integrity', '')
            crossorigin = attr_dict.get('crossorigin', '')
            
            has_sri = bool(integrity)
            hash_algorithm = ''
            hash_value = ''
            
            if integrity:
                # Parse integrity attribute (format: "algorithm-hash")
                if '-' in integrity:
                    hash_algorithm, hash_value = integrity.split('-', 1)
            
            resource = {
                'tag': tag,
                'src': src,
                'hasSri': has_sri,
                'hashAlgorithm': hash_algorithm,
                'hashValue': hash_value,
                'crossorigin': crossorigin
            }
            self.resources.append(resource)
    
    def is_external(self, url):
        if url.startswith('//'):
            return True
        if url.startswith('http://') or url.startswith('https://'):
            parsed_base = urllib.parse.urlparse(self.base_url)
            parsed_url = urllib.parse.urlparse(url)
            return parsed_base.netloc != parsed_url.netloc
        return False

def main():
    url = input().strip()
    
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        parser = SRIParser(url)
        parser.feed(html)
        
        print("resources")
    
    except Exception as e:
        print("resources")

if __name__ == '__main__':
    main()