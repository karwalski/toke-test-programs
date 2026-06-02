import sys
import json
import re

def parse_changelog():
    content = sys.stdin.read()
    lines = content.strip().split('\n')
    
    versions = []
    current_version = None
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        # Match version header like ## [1.2.0] - 2024-01-15
        version_match = re.match(r'^## \[([^\]]+)\] - (.+)$', line)
        if version_match:
            if current_version:
                versions.append(current_version)
            
            version_num = version_match.group(1)
            date = version_match.group(2)
            current_version = {
                "version": version_num,
                "date": date,
                "added": [],
                "changed": [],
                "fixed": [],
                "removed": []
            }
            current_section = None
            continue
        
        # Match section headers like ### Added
        section_match = re.match(r'^### (Added|Changed|Fixed|Removed)$', line)
        if section_match and current_version:
            current_section = section_match.group(1).lower()
            continue
        
        # Match list items like - New feature
        item_match = re.match(r'^- (.+)$', line)
        if item_match and current_version and current_section:
            item_text = item_match.group(1)
            current_version[current_section].append(item_text)
            continue
    
    # Add the last version if exists
    if current_version:
        versions.append(current_version)
    
    # Filter out empty arrays from output
    for version in versions:
        version_clean = {"version": version["version"], "date": version["date"]}
        for key in ["added", "changed", "fixed", "removed"]:
            if version[key]:
                version_clean[key] = version[key]
        versions[versions.index(version)] = version_clean
    
    return versions

if __name__ == "__main__":
    result = parse_changelog()
    print(json.dumps(result, separators=(',', ':')))