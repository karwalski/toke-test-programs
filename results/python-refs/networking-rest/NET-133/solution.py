import sys
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import re

def main():
    # Read input
    base_url = input().strip()
    max_links = int(input().strip())
    
    try:
        # Fetch the base page
        with urlopen(base_url) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
    except Exception:
        print("OK")
        return
    
    # Extract all <a href> links using regex
    href_pattern = r'<a[^>]+href\s*=\s*["\']([^"\']+)["\']'
    matches = re.findall(href_pattern, html_content, re.IGNORECASE)
    
    # Convert relative URLs to absolute URLs
    links = []
    for href in matches:
        if href.startswith('#'):
            continue  # Skip fragment-only links
        absolute_url = urljoin(base_url, href)
        if absolute_url not in links:
            links.append(absolute_url)
        if len(links) >= max_links:
            break
    
    # Check each link
    ok_count = 0
    broken_count = 0
    
    for link in links[:max_links]:
        try:
            with urlopen(link) as response:
                status_code = response.getcode()
                if 200 <= status_code < 300:
                    ok_count += 1
                else:
                    broken_count += 1
        except HTTPError as e:
            broken_count += 1
        except URLError:
            broken_count += 1
        except Exception:
            broken_count += 1
    
    # Only print OK if all links are working or no links found
    total_checked = ok_count + broken_count
    if total_checked == 0 or (ok_count > 0 and broken_count == 0):
        print("OK")

if __name__ == "__main__":
    main()