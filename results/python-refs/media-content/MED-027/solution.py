import sys

def wrap_text(text, width):
    if not text.strip():
        return ""
    
    words = text.split()
    if not words:
        return ""
    
    lines = []
    current_line = words[0]
    
    for word in words[1:]:
        if len(current_line) + 1 + len(word) <= width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return "\n".join(lines)

# Read input
lines = sys.stdin.read().splitlines()
width = int(lines[0])
text_lines = lines[1:]

# Process paragraphs
paragraphs = []
current_paragraph = []

for line in text_lines:
    if line.strip() == "":
        if current_paragraph:
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = []
        paragraphs.append("")
    else:
        current_paragraph.append(line.strip())

# Handle last paragraph if it doesn't end with blank line
if current_paragraph:
    paragraphs.append(" ".join(current_paragraph))

# Wrap each paragraph and output
output_parts = []
for paragraph in paragraphs:
    if paragraph == "":
        output_parts.append("")
    else:
        wrapped = wrap_text(paragraph, width)
        if wrapped:
            output_parts.append(wrapped)

# Remove trailing empty lines and print
result = "\n".join(output_parts).rstrip()
if result:
    print(result)