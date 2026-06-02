import os
import json
import re
import sys

def scan_file_for_webshells(filepath):
    """Scan a file for web shell signatures"""
    results = []
    
    # Define signature patterns
    signatures = {
        'eval_base64': re.compile(r'eval\s*\(\s*base64_decode\s*\(', re.IGNORECASE),
        'system_call': re.compile(r'system\s*\(', re.IGNORECASE),
        'passthru_call': re.compile(r'passthru\s*\(', re.IGNORECASE),
        'request_execution': re.compile(r'\$_REQUEST\s*\[.*?\]\s*\(', re.IGNORECASE)
    }
    
    severity_map = {
        'eval_base64': 'critical',
        'system_call': 'high',
        'passthru_call': 'high',
        'request_execution': 'critical'
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            for sig_type, pattern in signatures.items():
                if pattern.search(line):
                    # Truncate code snippet to 80 characters
                    code_snippet = line.strip()[:80]
                    
                    result = {
                        'file': filepath,
                        'line': line_num,
                        'signature_type': sig_type,
                        'severity': severity_map[sig_type],
                        'code_snippet': code_snippet
                    }
                    results.append(result)
                    
    except Exception:
        # Skip files that can't be read
        pass
    
    return results

def is_target_file(filename):
    """Check if file is a target type for scanning"""
    target_extensions = ['.php', '.asp', '.aspx', '.jsp', '.sh', '.bash']
    return any(filename.lower().endswith(ext) for ext in target_extensions)

def scan_directory(directory_path):
    """Scan directory recursively for web shell signatures"""
    all_results = []
    
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if is_target_file(file):
                    filepath = os.path.join(root, file)
                    results = scan_file_for_webshells(filepath)
                    all_results.extend(results)
    except Exception:
        # If directory doesn't exist or can't be accessed, return empty results
        pass
    
    return all_results

def main():
    # Read directory path from stdin
    directory_path = input().strip()
    
    # Scan for web shells
    results = scan_directory(directory_path)
    
    # Output as JSON
    print(json.dumps(results, indent=0, separators=(',', ':')))

if __name__ == "__main__":
    main()