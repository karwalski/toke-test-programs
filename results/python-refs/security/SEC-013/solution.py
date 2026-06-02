import sys
import re
import json
import html

def sanitize_html(content):
    removed_elements = []
    
    # Remove script tags and their content
    def remove_script_tags(text):
        pattern = r'<script[^>]*>.*?</script>'
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            removed_elements.append({"type": "script_tag", "content": match})
        return re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove event handlers from tags
    def remove_event_handlers(text):
        pattern = r'(\s+on\w+\s*=\s*["\'][^"\']*["\'])'
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            removed_elements.append({"type": "event_handler", "content": match.strip()})
        return re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove javascript: URLs
    def remove_javascript_urls(text):
        pattern = r'(href\s*=\s*["\']javascript:[^"\']*["\']|src\s*=\s*["\']javascript:[^"\']*["\'])'
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            removed_elements.append({"type": "javascript_url", "content": match})
        return re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove data: URIs
    def remove_data_uris(text):
        pattern = r'(href\s*=\s*["\']data:[^"\']*["\']|src\s*=\s*["\']data:[^"\']*["\'])'
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            removed_elements.append({"type": "data_uri", "content": match})
        return re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Apply all sanitization functions
    sanitized = remove_script_tags(content)
    sanitized = remove_event_handlers(sanitized)
    sanitized = remove_javascript_urls(sanitized)
    sanitized = remove_data_uris(sanitized)
    
    return sanitized, removed_elements

def main():
    # Read all HTML content from stdin
    html_content = sys.stdin.read()
    
    # Sanitize the HTML
    sanitized_html, removed_elements = sanitize_html(html_content)
    
    # Output sanitized HTML to stdout
    sys.stdout.write(sanitized_html)
    
    # Output JSON summary of removed elements to stderr
    summary = {"removed_elements": removed_elements}
    sys.stderr.write(json.dumps(summary) + '\n')

if __name__ == "__main__":
    main()