import sys
import re

def main():
    text = sys.stdin.read()
    pattern = r'```([^\n]*)\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    blocks = []
    for lang, code in matches:
        if code.endswith('\n'):
            code = code[:-1]
        blocks.append(f'lang: {lang}\n{code}')
    print('\n---\n'.join(blocks))

main()