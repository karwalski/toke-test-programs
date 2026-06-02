import json
import sys

for line in sys.stdin:
    line = line.strip()
    if line:
        data = json.loads(line)
        
        citation_parts = []
        
        # Author (Last, First)
        citation_parts.append(f"{data['author_last']}, {data['author_first']}.")
        
        # Title in quotes
        citation_parts.append(f'"{data["title"]}."')
        
        # Container and publication details
        container_parts = [data['container']]
        
        if data['volume']:
            container_parts.append(f"vol. {data['volume']}")
        
        if data['issue']:
            container_parts.append(f"no. {data['issue']}")
        
        container_parts.append(data['year'])
        
        if data['pages']:
            container_parts.append(f"pp. {data['pages']}")
        
        citation_parts.append(", ".join(container_parts) + ".")
        
        print(" ".join(citation_parts))