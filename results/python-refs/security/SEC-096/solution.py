import sys
import json
import re
import os

def analyze_config_file(file_path):
    issues = []
    
    if not os.path.exists(file_path):
        return issues
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except:
        return issues
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Parse key-value pairs (YAML style)
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            # Check for weak encryption configurations
            key_lower = key.lower()
            value_lower = value.lower()
            
            # CBC mode detection
            if 'mode' in key_lower or 'cipher' in key_lower or 'encryption' in key_lower:
                if 'cbc' in value_lower:
                    issues.append({
                        "line": line_num,
                        "config_key": key,
                        "value_redacted": "[REDACTED]",
                        "issue": "CBC mode encryption",
                        "severity": "medium",
                        "recommendation": "Use GCM or other authenticated encryption modes"
                    })
            
            # Static IV detection
            if 'iv' in key_lower or 'initialization' in key_lower:
                if len(value) > 0 and not value_lower in ['random', 'generate', 'auto']:
                    issues.append({
                        "line": line_num,
                        "config_key": key,
                        "value_redacted": "[REDACTED]",
                        "issue": "Static initialization vector",
                        "severity": "high",
                        "recommendation": "Generate random IV for each encryption operation"
                    })
            
            # Short key detection
            if 'key' in key_lower and ('size' in key_lower or 'length' in key_lower or 'bits' in key_lower):
                try:
                    key_size = int(value)
                    if key_size < 256:
                        issues.append({
                            "line": line_num,
                            "config_key": key,
                            "value_redacted": "[REDACTED]",
                            "issue": "Short encryption key",
                            "severity": "high",
                            "recommendation": "Use minimum 256-bit keys"
                        })
                except:
                    pass
            
            # Hardcoded salt detection
            if 'salt' in key_lower:
                if len(value) > 0 and not value_lower in ['random', 'generate', 'auto']:
                    issues.append({
                        "line": line_num,
                        "config_key": key,
                        "value_redacted": "[REDACTED]",
                        "issue": "Hardcoded salt",
                        "severity": "medium",
                        "recommendation": "Generate random salt for each operation"
                    })
            
            # Low iteration count for KDFs
            if 'iteration' in key_lower or 'rounds' in key_lower or ('pbkdf' in key_lower and 'count' in key_lower):
                try:
                    iterations = int(value)
                    if iterations < 10000:
                        issues.append({
                            "line": line_num,
                            "config_key": key,
                            "value_redacted": "[REDACTED]",
                            "issue": "Low KDF iteration count",
                            "severity": "medium",
                            "recommendation": "Use minimum 10000 iterations"
                        })
                except:
                    pass
    
    return issues

def main():
    file_path = sys.stdin.readline().strip()
    issues = analyze_config_file(file_path)
    print("[")

if __name__ == "__main__":
    main()