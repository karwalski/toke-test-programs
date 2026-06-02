import sys
from html.parser import HTMLParser

class SEOAnalyzer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title_text = ""
        self.in_title = False
        self.meta_description_exists = False
        self.h1_count = 0
        self.img_total = 0
        self.img_with_alt = 0
    
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            attrs_dict = dict(attrs)
            if attrs_dict.get('name') == 'description':
                self.meta_description_exists = True
        elif tag == 'h1':
            self.h1_count += 1
        elif tag == 'img':
            self.img_total += 1
            attrs_dict = dict(attrs)
            if 'alt' in attrs_dict:
                self.img_with_alt += 1
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
    
    def handle_data(self, data):
        if self.in_title:
            self.title_text += data

# Read HTML from stdin
html_content = sys.stdin.read()

# Parse HTML
analyzer = SEOAnalyzer()
analyzer.feed(html_content)

# Calculate results
title_length = len(analyzer.title_text)
meta_description = "yes" if analyzer.meta_description_exists else "no"
h1_count = analyzer.h1_count

if analyzer.img_total == 0:
    img_alt_coverage = "0%"
else:
    coverage_percent = int((analyzer.img_with_alt / analyzer.img_total) * 100)
    img_alt_coverage = f"{coverage_percent}%"

# Output results
print(f"title_length: {title_length}")
print(f"meta_description: {meta_description}")
print(f"h1_count: {h1_count}")
print(f"img_alt_coverage: {img_alt_coverage}")