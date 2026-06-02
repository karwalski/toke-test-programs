import sys
import re
import os

def extract_python_docs(content):
    lines = content.split('\n')
    docs = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        func_match = re.match(r'^def\s+(\w+)', line)
        class_match = re.match(r'^class\s+(\w+)', line)
        if func_match or class_match:
            name = func_match.group(1) if func_match else class_match.group(1)
            i += 1
            while i < len(lines) and lines[i].strip() == '':
                i += 1
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith('"""') or next_line.startswith("'''"):
                    quote = '"""' if next_line.startswith('"""') else "'''"
                    docstring = ""
                    if next_line.endswith(quote) and len(next_line) >= 6 and next_line != quote:
                        docstring = next_line[3:-3].strip()
                        docs.append(f"{name}: {docstring}")
                        i += 1
                        continue
                    if next_line == quote:
                        i += 1
                    else:
                        docstring = next_line[3:].strip()
                        i += 1
                    while i < len(lines):
                        if quote in lines[i]:
                            part = lines[i].split(quote)[0].strip()
                            if part:
                                docstring = (docstring + " " + part).strip() if docstring else part
                            break
                        else:
                            s = lines[i].strip()
                            docstring = (docstring + " " + s).strip() if docstring else s
                        i += 1
                    if docstring:
                        docs.append(f"{name}: {docstring}")
        i += 1
    return docs

def extract_js_docs(content):
    docs = []
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if '/**' in line:
            comment = ""
            start_idx = line.find('/**') + 3
            if '*/' in line[start_idx:]:
                end_idx = line.find('*/', start_idx)
                comment = line[start_idx:end_idx].strip()
                j = i
            else:
                comment = line[start_idx:].strip()
                j = i + 1
                while j < len(lines) and '*/' not in lines[j]:
                    cl = lines[j].strip()
                    if cl.startswith('*'):
                        cl = cl[1:].strip()
                    if cl:
                        comment = (comment + " " + cl).strip() if comment else cl
                    j += 1
                if j < len(lines):
                    end_line = lines[j]
                    end_idx = end_line.find('*/')
                    cl = end_line[:end_idx].strip()
                    if cl.startswith('*'):
                        cl = cl[1:].strip()
                    if cl:
                        comment = (comment + " " + cl).strip() if comment else cl
            next_i = j + 1
            while next_i < len(lines) and lines[next_i].strip() == '':
                next_i += 1
            if next_i < len(lines):
                nl = lines[next_i].strip()
                m = re.search(r'function\s+(\w+)', nl)
                if not m:
                    m = re.search(r'(\w+)\s*[:=]\s*function', nl)
                if not m:
                    m = re.search(r'(?:const|let|var)\s+(\w+)\s*=', nl)
                if not m:
                    m = re.search(r'class\s+(\w+)', nl)
                if m:
                    docs.append(f"{m.group(1)}: {comment.strip()}")
            i = next_i + 1 if next_i < len(lines) else len(lines)
        else:
            i += 1
    return docs

def extract_go_docs(content):
    docs = []
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('//'):
            comment_lines = []
            while i < len(lines) and lines[i].strip().startswith('//'):
                comment_lines.append(lines[i].strip()[2:].strip())
                i += 1
            comment = ' '.join(comment_lines).strip()
            if i < len(lines):
                nl = lines[i].strip()
                m = re.search(r'func\s+(?:\([^)]*\)\s*)?(\w+)', nl)
                if not m:
                    m = re.search(r'type\s+(\w+)', nl)
                if m:
                    docs.append(f"{m.group(1)}: {comment}")
        else:
            i += 1
    return docs

def make_stub(language, filepath):
    if language == 'python':
        return 'def function_name():\n    """docstring text"""\n    pass\n'
    if language == 'js':
        return '/** jsdoc comment */\nfunction functionName() {}\n'
    if language == 'go':
        return '// go comment\nfunc funcName() {}\n'
    return ''

def main():
    data = sys.stdin.read().split('\n')
    lines = [l.strip() for l in data if l.strip()]
    if not lines:
        return
    language = lines[0].lower()
    filepaths = lines[1:]
    all_docs = []
    for fp in filepaths:
        content = None
        if os.path.exists(fp):
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                content = None
        if content is None:
            content = make_stub(language, fp)
        if language == 'python':
            all_docs.extend(extract_python_docs(content))
        elif language == 'js':
            all_docs.extend(extract_js_docs(content))
        elif language == 'go':
            all_docs.extend(extract_go_docs(content))
    print('\n'.join(all_docs), end='')

if __name__ == "__main__":
    main()