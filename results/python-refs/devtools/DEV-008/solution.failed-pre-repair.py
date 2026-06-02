import sys
import re

def extract_python_docs(content):
    lines = content.split('\n')
    docs = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for function definition
        func_match = re.match(r'^def\s+(\w+)', line)
        class_match = re.match(r'^class\s+(\w+)', line)
        
        if func_match or class_match:
            name = func_match.group(1) if func_match else class_match.group(1)
            i += 1
            
            # Look for docstring on next lines
            while i < len(lines) and lines[i].strip() == '':
                i += 1
            
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith('"""') or next_line.startswith("'''"):
                    quote = '"""' if next_line.startswith('"""') else "'''"
                    docstring = ""
                    
                    # Single line docstring
                    if next_line.endswith(quote) and len(next_line) > 6:
                        docstring = next_line[3:-3].strip()
                        docs.append(f"{name}: {docstring}")
                        i += 1
                        continue
                    
                    # Multi-line docstring
                    if next_line == quote:
                        i += 1
                    else:
                        docstring = next_line[3:].strip()
                        i += 1
                    
                    while i < len(lines):
                        if lines[i].strip().endswith(quote):
                            if lines[i].strip() != quote:
                                if docstring:
                                    docstring += " " + lines[i].strip()[:-3].strip()
                                else:
                                    docstring = lines[i].strip()[:-3].strip()
                            break
                        else:
                            if docstring:
                                docstring += " " + lines[i].strip()
                            else:
                                docstring = lines[i].strip()
                        i += 1
                    
                    if docstring:
                        docs.append(f"{name}: {docstring}")
        
        i += 1
    
    return docs

def extract_docs(language, filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    if language.lower() == 'python':
        return extract_python_docs(content)
    
    # For other languages, look for /** */ comments
    docs = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Look for /** */ style comments
        if '/**' in line:
            comment = ""
            start_line = i
            
            # Single line comment
            if '*/' in line:
                start_idx = line.find('/**') + 3
                end_idx = line.find('*/')
                comment = line[start_idx:end_idx].strip()
            else:
                # Multi-line comment
                start_idx = line.find('/**') + 3
                comment = line[start_idx:].strip()
                
                j = i + 1
                while j < len(lines) and '*/' not in lines[j]:
                    clean_line = lines[j].strip()
                    if clean_line.startswith('*'):
                        clean_line = clean_line[1:].strip()
                    comment += " " + clean_line
                    j += 1
                
                if j < len(lines):
                    end_line = lines[j]
                    end_idx = end_line.find('*/')
                    clean_line = end_line[:end_idx].strip()
                    if clean_line.startswith('*'):
                        clean_line = clean_line[1:].strip()
                    comment += " " + clean_line
            
            # Look for function/class after comment
            next_i = start_line + (j - i + 1 if '*/' not in line else 1)
            while next_i < len(lines) and lines[next_i].strip() == '':
                next_i += 1
            
            if next_i < len(lines):
                next_line = lines[next_i].strip()
                func_match = re.search(r'(?:function|def)\s+(\w+)', next_line)
                class_match = re.search(r'class\s+(\w+)', next_line)
                
                if func_match:
                    docs.append(f"{func_match.group(1)}: {comment.strip()}")
                elif class_match:
                    docs.append(f"{class_match.group(1)}: {comment.strip()}")
    
    return docs

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if not lines:
        return
    
    language = lines[0]
    filepaths = lines[1:]
    
    all_docs = []
    for filepath in filepaths:
        docs = extract_docs(language, filepath)
        all_docs.extend(docs)
    
    for doc in all_docs:
        print(doc)

if __name__ == "__main__":
    main()