import sys

text = sys.stdin.read()
paragraphs = text.strip().split('\n\n')

for i, paragraph in enumerate(paragraphs, 1):
    print(f"=== PARA {i} ===")
    print(paragraph)