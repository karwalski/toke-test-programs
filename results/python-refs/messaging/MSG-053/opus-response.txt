import sys
import re

def convert(text):
    # Handle code blocks first (triple backticks)
    def code_block_repl(m):
        content = m.group(1)
        return '| ' + content
    text = re.sub(r'```(.*?)```', code_block_repl, text, flags=re.DOTALL)
    
    # Inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # Links [text](url) -> text (url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', text)
    
    lines = text.split('\n')
    result = []
    for line in lines:
        if line.startswith('#'):
            header = re.sub(r'^#+\s*', '', line).strip()
            result.append(header.upper())
        elif re.match(r'^\s*-\s+', line):
            line = re.sub(r'^(\s*)-(\s+)', r'\1*\2', line)
            result.append(line)
        else:
            # Strip bold and italic
            line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            line = re.sub(r'\*([^*]+)\*', r'\1', line)
            line = re.sub(r'__([^_]+)__', r'\1', line)
            line = re.sub(r'_([^_]+)_', r'\1', line)
            result.append(line)
    
    return '\n'.join(result)

text = sys.stdin.read()
print(convert(text))