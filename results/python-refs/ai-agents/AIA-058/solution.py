import sys
import json
import re

def extract_resume_data():
    content = sys.stdin.read().strip()
    lines = content.split('\n')
    
    result = {
        "name": "",
        "email": "",
        "phone": "",
        "skills": [],
        "experience": [],
        "education": []
    }
    
    # Extract name (first line)
    if lines:
        result["name"] = lines[0].strip().title()
    
    # Extract email and phone from contact line
    if len(lines) > 1:
        contact_line = lines[1]
        # Extract email
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', contact_line)
        if email_match:
            result["email"] = email_match.group(1)
        
        # Extract phone
        phone_match = re.search(r'(\d{3}-\d{4})', contact_line)
        if phone_match:
            result["phone"] = phone_match.group(1)
    
    # Find sections
    current_section = None
    for i, line in enumerate(lines):
        line = line.strip()
        
        if line.startswith('SKILLS:'):
            # Extract skills
            skills_text = line[7:].strip()
            result["skills"] = [skill.strip() for skill in skills_text.split(',')]
        elif line == 'EXPERIENCE':
            current_section = 'experience'
        elif line == 'EDUCATION':
            current_section = 'education'
        elif current_section == 'experience' and line:
            # Parse experience line
            # Format: "Role at Company (duration)"
            match = re.match(r'(.+?)\s+at\s+(.+?)\s+\((.+?)\)', line)
            if match:
                role, company, duration = match.groups()
                result["experience"].append({
                    "company": company,
                    "role": role,
                    "duration": duration
                })
        elif current_section == 'education' and line:
            # Parse education line
            # Format: "Degree, Institution, Year"
            parts = [part.strip() for part in line.split(',')]
            if len(parts) >= 3:
                degree = parts[0]
                institution = parts[1]
                year = parts[2]
                result["education"].append({
                    "institution": institution,
                    "degree": degree,
                    "year": year
                })
    
    return result

if __name__ == "__main__":
    data = extract_resume_data()
    print(json.dumps(data, separators=(',', ':')))