import json
import sys

def build_span_tree(spans):
    # Create a mapping of span_id to span
    span_map = {span['span_id']: span for span in spans}
    
    # Find root spans and build children mapping
    children = {}
    root_spans = []
    
    for span in spans:
        if span['parent_id'] is None:
            root_spans.append(span)
        else:
            parent_id = span['parent_id']
            if parent_id not in children:
                children[parent_id] = []
            children[parent_id].append(span)
    
    return root_spans, children

def print_span_tree(span, children, indent=0):
    # Calculate end time
    end_ms = span['start_ms'] + span['duration_ms']
    
    # Print current span with proper indentation
    indent_str = "  " * indent
    print(f"{indent_str}{span['service']}.{span['operation']} [{span['start_ms']}ms - {end_ms}ms]")
    
    # Print children recursively
    if span['span_id'] in children:
        for child in children[span['span_id']]:
            print_span_tree(child, children, indent + 1)

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    spans = json.loads(input_data)
    
    # Build span tree
    root_spans, children = build_span_tree(spans)
    
    # Print the tree starting from root spans
    for root_span in root_spans:
        print_span_tree(root_span, children)

if __name__ == "__main__":
    main()