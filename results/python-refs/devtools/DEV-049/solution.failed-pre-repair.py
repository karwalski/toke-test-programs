import sys

def count_lines(file_path, language):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return 0, 0
    
    comment_lines = 0
    code_lines = 0
    
    if language == 'python':
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('#'):
                comment_lines += 1
            else:
                code_lines += 1
    elif language == 'java' or language == 'c' or language == 'cpp':
        in_multiline_comment = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Handle multiline comments
            if '/*' in stripped:
                in_multiline_comment = True
            if '*/' in stripped:
                in_multiline_comment = False
                if stripped.startswith('/*') or stripped.startswith('*'):
                    comment_lines += 1
                else:
                    code_lines += 1
                continue
                
            if in_multiline_comment:
                comment_lines += 1
            elif stripped.startswith('//'):
                comment_lines += 1
            else:
                code_lines += 1
    elif language == 'javascript':
        in_multiline_comment = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            if '/*' in stripped:
                in_multiline_comment = True
            if '*/' in stripped:
                in_multiline_comment = False
                if stripped.startswith('/*') or stripped.startswith('*'):
                    comment_lines += 1
                else:
                    code_lines += 1
                continue
                
            if in_multiline_comment:
                comment_lines += 1
            elif stripped.startswith('//'):
                comment_lines += 1
            else:
                code_lines += 1
    
    return comment_lines, code_lines

def main():
    lines = sys.stdin.read().strip().split('\n')
    language = lines[0]
    file_paths = lines[1:]
    
    for file_path in file_paths:
        comment_lines, code_lines = count_lines(file_path, language)
        total_lines = comment_lines + code_lines
        
        if total_lines == 0:
            percentage = 0
        else:
            percentage = round((comment_lines / total_lines) * 100)
        
        print(f"{file_path}: {percentage}% comments ({comment_lines} comment / {total_lines} code lines)")

if __name__ == "__main__":
    main()