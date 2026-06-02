import sys

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

for line in sys.stdin:
    url = line.strip()
    if url:
        print(f'  <url><loc>{url}</loc></url>')

print('</urlset>')