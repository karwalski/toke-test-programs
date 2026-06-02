import sys

def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isspace():
            i += 1
        elif expression[i].isdigit() or expression[i] == '.':
            start = i
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                i += 1
            tokens.append(float(expression[start:i]))
        elif expression[i] in '+-*/^()':
            tokens.append(expression[i])
            i += 1
        else:
            i += 1
    return tokens

def get_precedence(op):
    if op in ['+', '-']:
        return 1
    elif op in ['*', '/']:
        return 2
    elif op == '^':
        return 3
    return 0

def is_right_associative(op):
    return op == '^'

def apply_operator(op, b, a):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
    elif op == '^':
        return a ** b

def evaluate_expression(tokens):
    values = []
    operators = []
    
    for token in tokens:
        if isinstance(token, float):
            values.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                values.append(apply_operator(operators.pop(), values.pop(), values.pop()))
            operators.pop()  # Remove '('
        elif token in '+-*/^':
            while (operators and operators[-1] != '(' and
                   (get_precedence(operators[-1]) > get_precedence(token) or
                    (get_precedence(operators[-1]) == get_precedence(token) and not is_right_associative(token)))):
                values.append(apply_operator(operators.pop(), values.pop(), values.pop()))
            operators.append(token)
    
    while operators:
        values.append(apply_operator(operators.pop(), values.pop(), values.pop()))
    
    return values[0]

expression = input().strip()
tokens = tokenize(expression)
result = evaluate_expression(tokens)

if result == int(result):
    print(int(result))
else:
    print(result)