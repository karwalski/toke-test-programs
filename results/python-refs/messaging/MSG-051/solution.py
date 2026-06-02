import sys
import json
import re

# Read input
lines = sys.stdin.read().strip().split('\n')
url = lines[0]
html_content = '\n'.join(lines[1:])

# Initialize result
result = {
    "url": url,
    "title": "",
    "description": "",
    "image": "",
    "site_name": ""
}

# Parse Open Graph meta tags
og_title_match = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', html_content)
if og_title_match:
    result["title"] = og_title_match.group(1)

og_description_match = re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', html_content)
if og_description_match:
    result["description"] = og_description_match.group(1)

og_image_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]*)"', html_content)
if og_image_match:
    result["image"] = og_image_match.group(1)

og_site_name_match = re.search(r'<meta\s+property="og:site_name"\s+content="([^"]*)"', html_content)
if og_site_name_match:
    result["site_name"] = og_site_name_match.group(1)

# Output JSON
print(json.dumps(result, separators=(',', ':')))