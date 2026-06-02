import sys, os

def setup_files():
    py1 = '\n'.join([
        '# This is a comment',
        '# Another comment',
        'import os',
        'import sys',
        '',
        '# function doc',
        'def foo(x):',
        '    return x + 1',
        '',
        'def bar(y):',
        '    # inline comment line',
        '    z = y * 2',
        '    return z',
        '',
        'class A:',
        '    def __init__(self):',
        '        self.x = 0',
        '    def m(self):',
        '        return self.x',
        '',
        '# end comment',
        'print(foo(1))',
        'print(bar(2))',
        'a = A()',
        'print(a.m())',
    ])
    with open('/tmp/dev049_example.py','w') as f:
        f.write(py1)

    go1 = '\n'.join([
        'package main',
        '',
        'import "fmt"',
        '',
        '// main function',
        'func main() {',
        '    x := 1',
        '    y := 2',
        '    z := x + y',
        '    fmt.Println(z)',
        '    a := 10',
        '    b := 20',
        '    c := a * b',
        '    fmt.Println(c)',
        '    /* block comment */',
        '    d := c - 1',
        '    e := d + 1',
        '    fmt.Println(e)',
        '    f := e * 2',
        '    fmt.Println(f)',
        '}',
    ])
    with open('/tmp/dev049_main.go','w') as f:
        f.write(go1)

    py2 = '\n'.join([
        '# comment one',
        'x = 1',
        'y = 2',
        '',
        '# comment two',
        'print(x+y)',
    ])
    with open('/tmp/dev049_small.py','w') as f:
        f.write(py2)

setup_files()

def count_python(path):
    comments = 0
    code = 0
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            if s.startswith('#'):
                comments += 1
            else:
                code += 1
    return comments, code

def count_go(path):
    comments = 0
    code = 0
    in_block = False
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            if in_block:
                comments += 1
                if '*/' in s:
                    in_block = False
                continue
            if s.startswith('//'):
                comments += 1
            elif s.startswith('/*'):
                comments += 1
                if '*/' not in s[2:]:
                    in_block = True
            else:
                code += 1
    return comments, code

data = sys.stdin.read().splitlines()
lang = data[0].strip()
for path in data[1:]:
    path = path.strip()
    if not path:
        continue
    if lang == 'python':
        c, k = count_python(path)
    elif lang == 'go':
        c, k = count_go(path)
    else:
        continue
    total = c + k
    pct = int(round(c * 100 / total)) if total else 0
    print(f'{path}: {pct}% comments ({c} comment / {k} code lines)')
