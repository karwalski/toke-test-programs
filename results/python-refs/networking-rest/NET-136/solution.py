#!/usr/bin/env python3

import sys
import json
import urllib.request
import urllib.error

def fetch_openapi_spec(base_url):
    """Fetch OpenAPI spec from the given base URL."""
    url = base_url.rstrip('/') + '/openapi.json'
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except (urllib.error.URLError, json.JSONDecodeError):
        return None

def extract_paths_and_schemas(spec):
    """Extract paths and schemas from OpenAPI spec."""
    if not spec:
        return {}, {}
    
    paths = spec.get('paths', {})
    schemas = spec.get('components', {}).get('schemas', {})
    
    return paths, schemas

def is_breaking_path_change(old_path, new_path, path_key):
    """Determine if a path change is breaking."""
    if not old_path or not new_path:
        return False
    
    # Check if required parameters were added
    old_params = old_path.get('parameters', [])
    new_params = new_path.get('parameters', [])
    
    old_required = set(p['name'] for p in old_params if p.get('required', False))
    new_required = set(p['name'] for p in new_params if p.get('required', False))
    
    if new_required - old_required:
        return True
    
    # Check if response schemas changed in breaking ways
    old_responses = old_path.get('responses', {})
    new_responses = new_path.get('responses', {})
    
    for status_code in old_responses:
        if status_code in new_responses:
            old_schema = old_responses[status_code].get('content', {}).get('application/json', {}).get('schema')
            new_schema = new_responses[status_code].get('content', {}).get('application/json', {}).get('schema')
            
            if old_schema != new_schema:
                return True
    
    return False

def is_breaking_schema_change(old_schema, new_schema):
    """Determine if a schema change is breaking."""
    if not old_schema or not new_schema:
        return False
    
    # Check if required fields were added
    old_required = set(old_schema.get('required', []))
    new_required = set(new_schema.get('required', []))
    
    if new_required - old_required:
        return True
    
    # Check if properties were removed
    old_properties = set(old_schema.get('properties', {}).keys())
    new_properties = set(new_schema.get('properties', {}).keys())
    
    if old_properties - new_properties:
        return True
    
    return False

def analyze_changes(old_paths, new_paths, old_schemas, new_schemas):
    """Analyze changes and categorize them."""
    breaking_changes = []
    non_breaking_changes = []
    removed_items = []
    added_items = []
    
    # Analyze path changes
    all_paths = set(old_paths.keys()) | set(new_paths.keys())
    
    for path in all_paths:
        if path in old_paths and path not in new_paths:
            removed_items.append(f"Path: {path}")
        elif path not in old_paths and path in new_paths:
            added_items.append(f"Path: {path}")
        elif path in old_paths and path in new_paths:
            for method in set(old_paths[path].keys()) | set(new_paths[path].keys()):
                if method in old_paths[path] and method not in new_paths[path]:
                    removed_items.append(f"Method: {method.upper()} {path}")
                elif method not in old_paths[path] and method in new_paths[path]:
                    added_items.append(f"Method: {method.upper()} {path}")
                elif method in old_paths[path] and method in new_paths[path]:
                    if is_breaking_path_change(old_paths[path][method], new_paths[path][method], f"{method.upper()} {path}"):
                        breaking_changes.append(f"Method: {method.upper()} {path}")
                    elif old_paths[path][method] != new_paths[path][method]:
                        non_breaking_changes.append(f"Method: {method.upper()} {path}")
    
    # Analyze schema changes
    all_schemas = set(old_schemas.keys()) | set(new_schemas.keys())
    
    for schema in all_schemas:
        if schema in old_schemas and schema not in new_schemas:
            removed_items.append(f"Schema: {schema}")
        elif schema not in old_schemas and schema in new_schemas:
            added_items.append(f"Schema: {schema}")
        elif schema in old_schemas and schema in new_schemas:
            if is_breaking_schema_change(old_schemas[schema], new_schemas[schema]):
                breaking_changes.append(f"Schema: {schema}")
            elif old_schemas[schema] != new_schemas[schema]:
                non_breaking_changes.append(f"Schema: {schema}")
    
    return breaking_changes, non_breaking_changes, removed_items, added_items

def main():
    # Read input
    old_url = input().strip()
    new_url = input().strip()
    
    # Fetch OpenAPI specs
    old_spec = fetch_openapi_spec(old_url)
    new_spec = fetch_openapi_spec(new_url)
    
    # Extract paths and schemas
    old_paths, old_schemas = extract_paths_and_schemas(old_spec)
    new_paths, new_schemas = extract_paths_and_schemas(new_spec)
    
    # Analyze changes
    breaking, non_breaking, removed, added = analyze_changes(old_paths, new_paths, old_schemas, new_schemas)
    
    # Output results
    print("BREAKING CHANGES")
    for change in breaking:
        print(change)
    
    if non_breaking:
        print("\nNON-BREAKING CHANGES")
        for change in non_breaking:
            print(change)
    
    if removed:
        print("\nREMOVED")
        for item in removed:
            print(item)
    
    if added:
        print("\nADDED")
        for item in added:
            print(item)

if __name__ == "__main__":
    main()