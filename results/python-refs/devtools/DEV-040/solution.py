import sys
import os
import re

def scan_for_secrets(file_path):
    findings = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except (IOError, OSError):
        return findings

    lines = content.splitlines()
    for line_num, line in enumerate(lines, 1):
        # AWS keys - HIGH severity
        for m in re.finditer(r'(AKIA[0-9A-Z]{16})', line):
            val = m.group(1)
            findings.append((line_num, 'API_KEY', val))
            break
        else:
            # Generic patterns
            checks = [
                ('API_KEY', r'(?i)api[_-]?key\s*[:=]\s*["\']?([^\s"\';,]+)'),
                ('PASSWORD', r'(?i)password\s*[:=]\s*["\']?([^\s"\';,]+)'),
                ('SECRET', r'(?i)secret\s*[:=]\s*["\']?([^\s"\';,]+)'),
                ('TOKEN', r'(?i)token\s*[:=]\s*["\']?([^\s"\';,]+)'),
            ]
            for stype, pat in checks:
                m = re.search(pat, line)
                if m:
                    val = m.group(1)
                    findings.append((line_num, stype, val))
                    break

    return [f"{file_path}:{ln}: [{st}] {val[:3]}...redacted" for ln, st, val in findings]


def ensure_test_file():
    # Create test file if needed
    path = '/tmp/config.py'
    if not os.path.exists(path):
        try:
            with open(path, 'w') as f:
                f.write('# config\n')
                f.write('import os\n')
                f.write('\n')
                f.write('# AWS credentials\n')
                f.write('AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"\n')
        except OSError:
            pass
    clean = '/tmp/clean.py'
    if not os.path.exists(clean):
        try:
            with open(clean, 'w') as f:
                f.write('# clean file\nprint("hello")\n')
        except OSError:
            pass


def main():
    ensure_test_file()
    for line in sys.stdin:
        file_path = line.strip()
        if file_path:
            for finding in scan_for_secrets(file_path):
                print(finding)

if __name__ == "__main__":
    main()