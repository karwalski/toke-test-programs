import sys
import re
from xml.parsers.expat import ParserCreate

def detect_xml_bomb():
    # Read all XML content from stdin
    xml_content = sys.stdin.read().strip()
    
    # Parse DOCTYPE and entity declarations
    entities = {}
    entity_refs = {}
    
    # Extract DOCTYPE section
    doctype_match = re.search(r'<!DOCTYPE[^>]*\[(.*?)\]>', xml_content, re.DOTALL)
    if doctype_match:
        doctype_content = doctype_match.group(1)
        
        # Find all entity declarations
        entity_pattern = r'<!ENTITY\s+(\w+)\s+"([^"]*)">'
        for match in re.finditer(entity_pattern, doctype_content):
            entity_name = match.group(1)
            entity_value = match.group(2)
            entities[entity_name] = entity_value
            
            # Count entity references in the value
            ref_count = len(re.findall(r'&(\w+);', entity_value))
            entity_refs[entity_name] = ref_count
    
    # Calculate expansion depth and size
    def calculate_expansion(entity_name, visited=None, depth=0):
        if visited is None:
            visited = set()
        
        if entity_name in visited:
            return depth, 1  # Circular reference
        
        if entity_name not in entities:
            return depth, 1
        
        visited.add(entity_name)
        entity_value = entities[entity_name]
        
        # Find all entity references in this entity's value
        refs = re.findall(r'&(\w+);', entity_value)
        
        if not refs:
            # Leaf entity - count characters
            visited.remove(entity_name)
            return depth + 1, len(entity_value)
        
        max_depth = depth + 1
        total_size = 0
        
        # Calculate size by replacing each reference
        remaining_text = entity_value
        for ref in refs:
            ref_depth, ref_size = calculate_expansion(ref, visited.copy(), depth + 1)
            max_depth = max(max_depth, ref_depth)
            total_size += ref_size
            # Remove the literal characters that aren't entity references
            remaining_text = remaining_text.replace(f'&{ref};', '', 1)
        
        # Add any literal characters
        total_size += len(remaining_text)
        
        visited.remove(entity_name)
        return max_depth, total_size
    
    # Find entity usage in the document body
    body_match = re.search(r'<[^!?][^>]*>(.*?)</[^>]*>', xml_content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
        body_refs = re.findall(r'&(\w+);', body_content)
        
        max_depth = 0
        max_size = 0
        example_chain = []
        
        for ref in body_refs:
            depth, size = calculate_expansion(ref)
            if depth > max_depth or size > max_size:
                max_depth = max(max_depth, depth)
                max_size = max(max_size, size)
                
                # Build example chain
                chain = []
                current = ref
                visited_chain = set()
                
                while current in entities and current not in visited_chain:
                    chain.append(current)
                    visited_chain.add(current)
                    entity_value = entities[current]
                    refs_in_value = re.findall(r'&(\w+);', entity_value)
                    if refs_in_value:
                        current = refs_in_value[0]  # Take first reference
                    else:
                        break
                
                example_chain = chain
        
        # Determine if vulnerable
        # Consider vulnerable if expansion depth > 2 or size > 16
        if max_depth > 2 or max_size > 16:
            chain_str = " -> ".join(example_chain) if example_chain else "none"
            print(f"VULNERABLE expansion_depth={max_depth}, estimated_expanded_size={max_size}, example_chain={chain_str}")
        else:
            print("SAFE")
    else:
        print("SAFE")

if __name__ == "__main__":
    detect_xml_bomb()