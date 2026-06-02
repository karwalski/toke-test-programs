import sys
import re

def scan_file_for_comments(filepath):
    """Scan a file for TODO, FIXME, HACK, and XXX comments."""
    results = []
    keywords = ['TODO', 'FIXME', 'HACK', 'XXX']
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                # Look for comments containing our keywords
                for keyword in keywords:
                    # Match comment patterns with the keyword
                    # Handle # comments (Python, shell, etc.)
                    hash_pattern = r'#.*?\b' + keyword + r'\b(.*)$'
                    # Handle // comments (C++, Java, etc.)
                    slash_pattern = r'//.*?\b' + keyword + r'\b(.*)$'
                    # Handle /* */ comments (C, Java, etc.)
                    block_pattern = r'/\*.*?\b' + keyword + r'\b(.*?)\*/'
                    
                    for pattern in [hash_pattern, slash_pattern, block_pattern]:
                        match = re.search(pattern, line, re.IGNORECASE)
                        if match:
                            # Extract the comment text after the keyword
                            comment_text = match.group(1).strip()
                            # Remove any trailing */ from block comments
                            comment_text = re.sub(r'\s*\*/$', '', comment_text)
                            # Clean up the comment text
                            comment_text = comment_text.lstrip(':').strip()
                            
                            results.append((filepath, line_num, keyword.upper(), comment_text))
                            break  # Only match first keyword per line
    
    except (IOError, OSError):
        # Skip files that can't be read
        pass
    
    return results

def main():
    all_results = []
    
    # Read file paths from stdin
    for line in sys.stdin:
        filepath = line.strip()
        if filepath:
            results = scan_file_for_comments(filepath)
            all_results.extend(results)
    
    # Sort by file path, then by line number
    all_results.sort(key=lambda x: (x[0], x[1]))
    
    # Print results in the required format
    for filepath, line_num, keyword, comment_text in all_results:
        print(f"{filepath}:{line_num}: [{keyword}] {comment_text}")

if __name__ == "__main__":
    main()