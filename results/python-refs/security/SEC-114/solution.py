import sys
import urllib.request
import urllib.parse
import json
import time

def main():
    # Read input
    url = input().strip()
    method = input().strip()
    body_template = input().strip()
    
    # Define fuzz payloads
    payloads = [
        ("boundary_negative", "-1"),
        ("boundary_zero", "0"),
        ("boundary_large", "999999999"),
        ("type_confusion_int", "123"),
        ("type_confusion_bool", "true"),
        ("type_confusion_null", "null"),
        ("format_string", "%s%s%s"),
        ("special_chars", "<script>alert(1)</script>"),
        ("special_chars", "' OR 1=1 --"),
        ("special_chars", "../../../etc/passwd"),
        ("unicode", "\\u0000\\u0001\\u0002"),
        ("long_string", "A" * 10000)
    ]
    
    results = []
    
    # Print summary
    print("Summary:")

if __name__ == "__main__":
    main()