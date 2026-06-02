import csv
import json
import sys

def build_tree():
    # Read CSV from stdin
    reader = csv.DictReader(sys.stdin)
    
    # Store relationships
    children = {}
    all_batches = set()
    
    for row in reader:
        child = row['child_batch']
        parent = row['parent_batch']
        step = row['step']
        
        all_batches.add(child)
        all_batches.add(parent)
        
        if parent not in children:
            children[parent] = []
        
        children[parent].append({
            'batch': child,
            'step': step
        })
    
    # Find root nodes (batches that are never children)
    child_batches = set()
    for parent in children:
        for child_info in children[parent]:
            child_batches.add(child_info['batch'])
    
    roots = all_batches - child_batches
    
    def build_subtree(batch):
        result = []
        if batch in children:
            for child_info in children[batch]:
                child_batch = child_info['batch']
                step = child_info['step']
                result.append({
                    'batch': child_batch,
                    'step': step,
                    'children': build_subtree(child_batch)
                })
        return result
    
    # Build the final tree
    tree = {}
    for root in roots:
        tree[root] = {
            'children': build_subtree(root)
        }
    
    return tree

# Generate and output the tree
tree = build_tree()
print(json.dumps(tree, separators=(',', ':')))