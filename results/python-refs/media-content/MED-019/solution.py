import json
import sys

for line in sys.stdin:
    data = json.loads(line.strip())
    
    author = f"{data['author_last']}, {data['author_first']}"
    year = data['year']
    title = data['title']
    journal = data['journal']
    volume = data['volume']
    issue = data['issue']
    pages = data['pages']
    
    citation = f"{author} ({year}). {title}. {journal}, {volume}({issue}), {pages}."
    print(citation)