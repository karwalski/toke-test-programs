import sys

def strip_comments(language, code_lines):
    if language == 'python':
        return strip_python_comments(code_lines)
    elif language == 'c':
        return strip_c_comments(code_lines)
    elif language == 'html':
        return strip_html_comments(code_lines)
    return code_lines

def strip_python_comments(lines):
    result = []
    for line in lines:
        # Find # that's not inside a string
        in_single_quote = False
        in_double_quote = False
        i = 0
        while i < len(line):
            char = line[i]
            if char == "'" and not in_double_quote:
                if i == 0 or line[i-1] != '\\':
                    in_single_quote = not in_single_quote
            elif char == '"' and not in_single_quote:
                if i == 0 or line[i-1] != '\\':
                    in_double_quote = not in_double_quote
            elif char == '#' and not in_single_quote and not in_double_quote:
                line = line[:i].rstrip()
                break
            i += 1
        result.append(line)
    return result

def strip_c_comments(lines):
    result = []
    in_block_comment = False
    
    for line in lines:
        new_line = ""
        i = 0
        while i < len(line):
            if in_block_comment:
                if i < len(line) - 1 and line[i:i+2] == '*/':
                    in_block_comment = False
                    i += 2
                    continue
                i += 1
            else:
                if i < len(line) - 1 and line[i:i+2] == '/*':
                    in_block_comment = True
                    i += 2
                    continue
                elif i < len(line) - 1 and line[i:i+2] == '//':
                    break
                else:
                    new_line += line[i]
                    i += 1
        
        if not in_block_comment:
            result.append(new_line.rstrip())
        else:
            result.append("")
    
    return result

def strip_html_comments(lines):
    result = []
    in_comment = False
    
    for line in lines:
        new_line = ""
        i = 0
        while i < len(line):
            if in_comment:
                if i < len(line) - 2 and line[i:i+3] == '-->':
                    in_comment = False
                    i += 3
                    continue
                i += 1
            else:
                if i < len(line) - 3 and line[i:i+4] == '<!--':
                    in_comment = True
                    i += 4
                    continue
                else:
                    new_line += line[i]
                    i += 1
        
        result.append(new_line.rstrip())
    
    return result

# Read input
lines = sys.stdin.read().strip().split('\n')
language = lines[0]
code_lines = lines[1:]

# Process and output
result_lines = strip_comments(language, code_lines)
for line in result_lines:
    print(line)