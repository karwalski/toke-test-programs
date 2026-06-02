import sys
import json
import os
from datetime import datetime
import re

def parse_timestamp(timestamp_str):
    """Parse various timestamp formats"""
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y/%m/%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S.%fZ'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue
    return None

def extract_timestamp(line):
    """Extract timestamp from log line"""
    # Common timestamp patterns
    patterns = [
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?)',
        r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})',
        r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})',
        r'(\d{1,2}/\d{1,2}/\d{4} \d{2}:\d{2}:\d{2})',
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            return match.group(1)
    return None

def extract_sequence_number(line):
    """Extract sequence number from log line"""
    # Look for patterns like [123], #123, seq:123, id:123
    patterns = [
        r'\[(\d+)\]',
        r'#(\d+)',
        r'seq[:\s]+(\d+)',
        r'id[:\s]+(\d+)',
        r'sequence[:\s]+(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None

def check_log_integrity(log_path):
    """Analyze log file for signs of tampering"""
    issues = []
    
    # Check if file exists
    if not os.path.exists(log_path):
        return {
            "integrity": "tampered",
            "issues": [{"lineNumber": 0, "type": "file_not_found", "description": "Log file does not exist"}],
            "summary": "Log file not found"
        }
    
    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        return {
            "integrity": "tampered",
            "issues": [{"lineNumber": 0, "type": "read_error", "description": f"Cannot read log file: {str(e)}"}],
            "summary": "Cannot read log file"
        }
    
    if not lines:
        return {
            "integrity": "intact",
            "issues": [],
            "summary": "Empty log file"
        }
    
    current_time = datetime.now()
    last_timestamp = None
    last_seq_num = None
    expected_seq_num = 1
    has_sequence_numbers = False
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
            
        # Extract timestamp
        timestamp_str = extract_timestamp(line)
        if timestamp_str:
            timestamp = parse_timestamp(timestamp_str)
            if timestamp:
                # Check for future timestamps
                if timestamp > current_time:
                    issues.append({
                        "lineNumber": line_num,
                        "type": "future_timestamp",
                        "description": f"Entry has future timestamp: {timestamp_str}"
                    })
                
                # Check for out-of-order timestamps
                if last_timestamp and timestamp < last_timestamp:
                    issues.append({
                        "lineNumber": line_num,
                        "type": "out_of_order",
                        "description": f"Timestamp out of order: {timestamp_str} comes after {last_timestamp}"
                    })
                
                last_timestamp = timestamp
        
        # Extract sequence number
        seq_num = extract_sequence_number(line)
        if seq_num is not None:
            has_sequence_numbers = True
            
            # Check for missing sequence numbers
            if last_seq_num is not None:
                if seq_num != expected_seq_num:
                    if seq_num < last_seq_num:
                        issues.append({
                            "lineNumber": line_num,
                            "type": "sequence_regression",
                            "description": f"Sequence number regression: {seq_num} after {last_seq_num}"
                        })
                    elif seq_num > expected_seq_num:
                        missing_count = seq_num - expected_seq_num
                        issues.append({
                            "lineNumber": line_num,
                            "type": "missing_sequence",
                            "description": f"Missing {missing_count} sequence number(s) before {seq_num}"
                        })
            
            last_seq_num = seq_num
            expected_seq_num = seq_num + 1
        
        # Check for suspicious deletion patterns
        if 'delete' in line.lower() or 'remove' in line.lower() or 'clear' in line.lower():
            if 'log' in line.lower() or 'history' in line.lower() or 'audit' in line.lower():
                issues.append({
                    "lineNumber": line_num,
                    "type": "suspicious_deletion",
                    "description": "Suspicious deletion activity detected"
                })
    
    # Determine overall integrity
    if not issues:
        integrity = "intact"
        summary = "Log integrity verified"
    elif any(issue["type"] in ["sequence_regression", "future_timestamp", "suspicious_deletion"] for issue in issues):
        integrity = "tampered"
        summary = f"Log shows signs of tampering ({len(issues)} issues found)"
    else:
        integrity = "suspicious"
        summary = f"Log integrity questionable ({len(issues)} issues found)"
    
    return {
        "integrity": integrity,
        "issues": issues,
        "summary": summary
    }

def main():
    try:
        log_path = input().strip()
        result = check_log_integrity(log_path)
        
        if result["integrity"] == "intact" and not result["issues"]:
            print("intact")
        else:
            print(json.dumps(result))
            
    except Exception as e:
        error_result = {
            "integrity": "tampered",
            "issues": [{"lineNumber": 0, "type": "error", "description": str(e)}],
            "summary": "Error analyzing log file"
        }
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()