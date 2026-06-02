import sys
import re

def detect_xml_bomb():
    xml_content = sys.stdin.read().strip()
    
    entities = {}
    
    doctype_match = re.search(r'<!DOCTYPE[^>]*\[(.*?)\]>', xml_content, re.DOTALL)
    if doctype_match:
        doctype_content = doctype_match.group(1)
        entity_pattern = r'<!ENTITY\s+(\w+)\s+"([^"]*)"\s*>'
        for match in re.finditer(entity_pattern, doctype_content):
            entities[match.group(1)] = match.group(2)
    
    if not entities:
        print("SAFE")
        return
    
    # Compute expanded size for each entity
    sizes = {}
    depths = {}
    
    def compute(name, stack):
        if name in stack:
            return float('inf'), float('inf')
        if name in sizes:
            return sizes[name], depths[name]
        if name not in entities:
            return 1, 0
        
        value = entities[name]
        refs = re.findall(r'&(\w+);', value)
        literal = re.sub(r'&\w+;', '', value)
        
        total_size = len(literal)
        max_depth = 0
        stack.add(name)
        for r in refs:
            rsize, rdepth = compute(r, stack)
            total_size += rsize
            if rdepth + 1 > max_depth:
                max_depth = rdepth + 1
        stack.remove(name)
        
        sizes[name] = total_size
        depths[name] = max_depth
        return total_size, max_depth
    
    max_size = 0
    max_depth = 0
    worst_entity = None
    
    for name in entities:
        s, d = compute(name, set())
        if s > max_size:
            max_size = s
            worst_entity = name
        if d > max_depth:
            max_depth = d
    
    # Find references in body
    body = re.sub(r'<!DOCTYPE[^>]*\[.*?\]>', '', xml_content, flags=re.DOTALL)
    body_refs = re.findall(r'&(\w+);', body)
    
    body_size = 0
    for r in body_refs:
        if r in entities:
            body_size += sizes.get(r, 0)
    
    # Vulnerability heuristic: nested entity refs (entity refs another entity) or large expansion
    has_nested = False
    for name, value in entities.items():
        refs = re.findall(r'&(\w+);', value)
        for r in refs:
            if r in entities:
                has_nested = True
                break
    
    if has_nested or max_size > 1024*1024 or body_size > 1024*1024:
        print("VULNERABLE")
    else:
        print("SAFE")

if __name__ == "__main__":
    detect_xml_bomb()