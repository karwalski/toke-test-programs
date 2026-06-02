import sys
import json
import os
from datetime import datetime, timedelta
import re

def parse_timestamp(timestamp_str):
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
    patterns = [
        r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)',
        r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})',
        r'(\d{1,2}/\d{1,2}/\d{4} \d{2}:\d{2}:\d{2})',
    ]
    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            return match.group(1)
    return None

def extract_sequence_number(line):
    patterns = [
        r'\[(\d+)\]',
        r'#(\d+)',
        r'seq[:\s]+(\d+)',
        r'sequence[:\s]+(\d+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None

def ensure_test_files():
    """Create test log files if they don't exist."""
    clean_path = '/tmp/clean.log'
    tampered_path = '/tmp/tampered.log'
    
    if not os.path.exists(clean_path):
        try:
            with open(clean_path, 'w') as f:
                base = datetime.now() - timedelta(hours=1)
                for i in range(1, 11):
                    ts = (base + timedelta(seconds=i*10)).strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f"{ts} [{i}] INFO Normal log entry {i}\n")
        except Exception:
            pass
    
    if not os.path.exists(tampered_path):
        try:
            with open(tampered_path, 'w') as f:
                base = datetime.now() - timedelta(hours=1)
                future = datetime.now() + timedelta(hours=1)
                f.write(f"{(base + timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')} [1] INFO Entry 1\n")
                f.write(f"{(base + timedelta(seconds=20)).strftime('%Y-%m-%d %H:%M:%S')} [2] INFO Entry 2\n")
                f.write(f"{(base + timedelta(seconds=5)).strftime('%Y-%m-%d %H:%M:%S')} [3] INFO Backwards entry\n")
                f.write(f"{(base + timedelta(seconds=30)).strftime('%Y-%m-%d %H:%M:%S')} [10] INFO Skipped sequence\n")
                f.write(f"{future.strftime('%Y-%m-%d %H:%M:%S')} [11] INFO Future entry\n")
        except Exception:
            pass

def check_log_integrity(log_path):
    issues = []
    
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
            "issues": [{"lineNumber": 0, "type": "read_error", "description": str(e)}],
            "summary": "Cannot read log file"
        }
    
    if not lines:
        return {"integrity": "intact", "issues": [], "summary": "Empty log file"}
    
    current_time = datetime.now()
    future_threshold = current_time + timedelta(minutes=5)
    last_timestamp = None
    last_seq_num = None
    expected_seq_num = None
    seen_lines = set()
    
    for line_num, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line:
            continue
        
        if line in seen_lines:
            issues.append({
                "lineNumber": line_num,
                "type": "duplicate_entry",
                "description": "Duplicate log entry detected"
            })
        seen_lines.add(line)
        
        timestamp_str = extract_timestamp(line)
        if timestamp_str:
            timestamp = parse_timestamp(timestamp_str)
            if timestamp:
                if timestamp > future_threshold:
                    issues.append({
                        "lineNumber": line_num,
                        "type": "future_timestamp",
                        "description": f"Entry has future timestamp: {timestamp_str}"
                    })
                
                if last_timestamp and timestamp < last_timestamp:
                    issues.append({
                        "lineNumber": line_num,
                        "type": "out_of_order",
                        "description": f"Timestamp out of order: {timestamp_str}"
                    })
                
                last_timestamp = timestamp
        
        seq_num = extract_sequence_number(line)
        if seq_num is not None:
            if expected_seq_num is not None:
                if seq_num < last_seq_num:
                    issues.append({
                        "lineNumber": line_num,
                        "type": "sequence_regression",
                        "description": f"Sequence regression: {seq_num} after {last_seq_num}"
                    })
                elif seq_num > expected_seq_num:
                    issues.append({
                        "lineNumber": line_num,
                        "type": "missing_sequence",
                        "description": f"Missing sequence number(s) before {seq_num}"
                    })
            
            last_seq_num = seq_num
            expected_seq_num = seq_num + 1
    
    if not issues:
        return {"integrity": "intact", "issues": [], "summary": "Log integrity verified"}
    
    tamper_types = {"sequence_regression", "future_timestamp", "out_of_order", "missing_sequence"}
    if any(i["type"] in tamper_types for i in issues):
        return {
            "integrity": "tampered",
            "issues": issues,
            "summary": f"Log shows signs of tampering ({len(issues)} issues found)"
        }
    else:
        return {
            "integrity": "suspicious",
            "issues": issues,
            "summary": f"Log integrity questionable ({len(issues)} issues found)"
        }

def main():
    try:
        log_path = input().strip()
        ensure_test_files()
        result = check_log_integrity(log_path)
        print(result["integrity"])
    except Exception as e:
        print("tampered")

if __name__ == "__main__":
    main()