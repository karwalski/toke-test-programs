import sys
import html
import re
import textwrap

def html_to_text(html_content):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_content)
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Clean up whitespace
    text = ' '.join(text.split())
    
    return text

def main():
    # Read HTML content from stdin
    html_content = sys.stdin.read().strip()
    
    # Convert to plain text
    plain_text = html_to_text(html_content)
    
    # Wrap at 72 characters
    wrapped_text = textwrap.fill(plain_text, width=72)
    
    # Output to stdout
    print(wrapped_text)

if __name__ == "__main__":
    main()