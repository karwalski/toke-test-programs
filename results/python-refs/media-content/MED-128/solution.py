import sys
import json
import xml.etree.ElementTree as ET

def xml_to_dict(element):
    result = {}
    
    # If element has children
    if len(element) > 0:
        for child in element:
            child_dict = xml_to_dict(child)
            result[child.tag] = child_dict[child.tag] if child.tag in child_dict else child_dict
        return {element.tag: result}
    else:
        # Leaf node - return the text content
        return {element.tag: element.text if element.text else ""}

def main():
    # Read XML from stdin
    xml_input = sys.stdin.read().strip()
    
    # Parse XML
    root = ET.fromstring(xml_input)
    
    # Convert to dictionary
    result_dict = xml_to_dict(root)
    
    # Convert to JSON and print
    json_output = json.dumps(result_dict, separators=(',', ':'))
    print(json_output)

if __name__ == "__main__":
    main()