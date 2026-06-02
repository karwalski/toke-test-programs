import json
import sys

def generate_certificate(data):
    name = data["name"]
    course = data["course"]
    date = data["date"]
    issuer = data["issuer"]
    
    # Certificate width is 28 characters (based on expected output)
    width = 28
    
    # Create the certificate lines
    lines = []
    
    # Top border
    lines.append("*" * width)
    
    # Title line
    title = "CERTIFICATE OF COMPLETION"
    padding = (width - 2 - len(title)) // 2
    title_line = "*" + " " * padding + title + " " * (width - 2 - padding - len(title)) + "*"
    lines.append(title_line)
    
    # Empty line
    empty_line = "*" + " " * (width - 2) + "*"
    lines.append(empty_line)
    
    # Name line
    name_line = "*  " + name + " " * (width - 3 - len(name)) + "*"
    lines.append(name_line)
    
    # Course line
    course_line = "*  " + course + " " * (width - 3 - len(course)) + "*"
    lines.append(course_line)
    
    # Date line
    date_line = "*  " + date + " " * (width - 3 - len(date)) + "*"
    lines.append(date_line)
    
    # Issuer line
    issuer_line = "*  " + issuer + " " * (width - 3 - len(issuer)) + "*"
    lines.append(issuer_line)
    
    # Bottom border
    lines.append("*" * width)
    
    return "\n".join(lines)

# Read input from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

# Generate and print certificate
certificate = generate_certificate(data)
print(certificate)