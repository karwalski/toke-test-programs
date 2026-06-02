import sys
import re

def identify_license(content):
    """Identify license from file content using common patterns"""
    
    # Normalize content for matching
    content_lower = content.lower()
    
    # MIT License patterns
    mit_patterns = [
        r'mit license',
        r'permission is hereby granted, free of charge',
        r'the above copyright notice and this permission notice',
        r'mit\s*$',
        r'massachusetts institute of technology'
    ]
    
    # Apache 2.0 patterns
    apache_patterns = [
        r'apache license.*version 2\.0',
        r'apache-2\.0',
        r'licensed under the apache license',
        r'www\.apache\.org/licenses/license-2\.0'
    ]
    
    # GPL patterns
    gpl_patterns = [
        r'gnu general public license.*version 3',
        r'gpl-3\.0',
        r'gnu gplv3',
        r'www\.gnu\.org/licenses/gpl-3\.0'
    ]
    
    # BSD patterns
    bsd_patterns = [
        r'bsd license',
        r'berkeley software distribution',
        r'redistribution and use in source and binary forms'
    ]
    
    # ISC patterns
    isc_patterns = [
        r'isc license',
        r'permission to use, copy, modify, and/or distribute'
    ]
    
    # Check for MIT
    for pattern in mit_patterns:
        if re.search(pattern, content_lower):
            return 'MIT'
    
    # Check for Apache 2.0
    for pattern in apache_patterns:
        if re.search(pattern, content_lower):
            return 'Apache-2.0'
    
    # Check for GPL-3.0
    for pattern in gpl_patterns:
        if re.search(pattern, content_lower):
            return 'GPL-3.0'
    
    # Check for BSD
    for pattern in bsd_patterns:
        if re.search(pattern, content_lower):
            return 'BSD-3-Clause'
    
    # Check for ISC
    for pattern in isc_patterns:
        if re.search(pattern, content_lower):
            return 'ISC'
    
    return 'UNKNOWN'

def main():
    # Read file path from stdin
    file_path = sys.stdin.read().strip()
    
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Identify license
        license_id = identify_license(content)
        print(license_id)
        
    except Exception:
        print('UNKNOWN')

if __name__ == '__main__':
    main()