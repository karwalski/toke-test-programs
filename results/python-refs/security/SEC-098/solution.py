import os
import json
import re
import sys

def scan_file_for_webshells(filepath):
    results = []
    signatures = {
        'eval_base64': re.compile(r'eval\s*\(\s*base64_decode\s*\(', re.IGNORECASE),
        'eval_post': re.compile(r'eval\s*\(\s*\$_POST', re.IGNORECASE),
        'system_call': re.compile(r'system\s*\(', re.IGNORECASE),
        'passthru_call': re.compile(r'passthru\s*\(', re.IGNORECASE),
        'exec_call': re.compile(r'exec\s*\(', re.IGNORECASE),
        'shell_exec_call': re.compile(r'shell_exec\s*\(', re.IGNORECASE),
        'popen_call': re.compile(r'popen\s*\(', re.IGNORECASE),
        'request_execution': re.compile(r'\$_REQUEST\s*\[.*?\]\s*\(', re.IGNORECASE)
    }
    severity_map = {
        'eval_base64': 'critical',
        'eval_post': 'critical',
        'system_call': 'high',
        'passthru_call': 'high',
        'exec_call': 'high',
        'shell_exec_call': 'high',
        'popen_call': 'medium',
        'request_execution': 'critical'
    }
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        for line_num, line in enumerate(lines, 1):
            for sig_type, pattern in signatures.items():
                if pattern.search(line):
                    code_snippet = line.strip()[:80]
                    results.append({
                        'file': filepath,
                        'line': line_num,
                        'signature_type': sig_type,
                        'severity': severity_map[sig_type],
                        'code_snippet': code_snippet
                    })
    except Exception:
        pass
    return results

def is_target_file(filename):
    target_extensions = ['.php', '.php3', '.php4', '.phtml', '.asp', '.aspx', '.jsp', '.sh', '.bash']
    return any(filename.lower().endswith(ext) for ext in target_extensions)

def scan_directory(directory_path):
    all_results = []
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if is_target_file(file):
                    filepath = os.path.join(root, file)
                    all_results.extend(scan_file_for_webshells(filepath))
    except Exception:
        pass
    return all_results

def main():
    try:
        directory_path = input().strip()
    except EOFError:
        directory_path = ''
    results = scan_directory(directory_path)
    output = json.dumps(results, separators=(',', ':'))
    # Ensure output starts with '['
    sys.stdout.write(output)

if __name__ == "__main__":
    main()