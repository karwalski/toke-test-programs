import json
import sys
import re

def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isspace():
            i += 1
        elif expression[i:i+3] == 'AND':
            tokens.append('AND')
            i += 3
        elif expression[i:i+2] == 'OR':
            tokens.append('OR')
            i += 2
        elif expression[i:i+3] == 'NOT':
            tokens.append('NOT')
            i += 3
        elif expression[i:i+2] == '>=':
            tokens.append('>=')
            i += 2
        elif expression[i:i+2] == '<=':
            tokens.append('<=')
            i += 2
        elif expression[i:i+2] == '!=':
            tokens.append('!=')
            i += 2
        elif expression[i] in '=<>()':
            tokens.append(expression[i])
            i += 1
        elif expression[i] == '"':
            j = i + 1
            while j < len(expression) and expression[j] != '"':
                j += 1
            tokens.append(expression[i:j+1])
            i = j + 1
        else:
            j = i
            while j < len(expression) and expression[j] not in ' =<>()' and not expression[j:j+2] in ['>=', '<=', '!='] and not expression[j:j+2] == 'OR' and not expression[j:j+3] in ['AND', 'NOT']:
                j += 1
            tokens.append(expression[i:j])
            i = j
    return tokens

def parse_expression(tokens):
    def parse_or():
        left = parse_and()
        while tokens and tokens[0] == 'OR':
            tokens.pop(0)
            right = parse_and()
            left = ('OR', left, right)
        return left
    
    def parse_and():
        left = parse_not()
        while tokens and tokens[0] == 'AND':
            tokens.pop(0)
            right = parse_not()
            left = ('AND', left, right)
        return left
    
    def parse_not():
        if tokens and tokens[0] == 'NOT':
            tokens.pop(0)
            return ('NOT', parse_comparison())
        return parse_comparison()
    
    def parse_comparison():
        if tokens and tokens[0] == '(':
            tokens.pop(0)
            result = parse_or()
            tokens.pop(0)  # remove ')'
            return result
        
        left = tokens.pop(0)
        op = tokens.pop(0)
        right = tokens.pop(0)
        
        if right.startswith('"') and right.endswith('"'):
            right = right[1:-1]
        elif right.isdigit():
            right = int(right)
        elif right.replace('.', '').isdigit():
            right = float(right)
        
        return ('COMP', left, op, right)
    
    return parse_or()

def evaluate(ast, obj):
    if ast[0] == 'AND':
        return evaluate(ast[1], obj) and evaluate(ast[2], obj)
    elif ast[0] == 'OR':
        return evaluate(ast[1], obj) or evaluate(ast[2], obj)
    elif ast[0] == 'NOT':
        return not evaluate(ast[1], obj)
    elif ast[0] == 'COMP':
        field, op, value = ast[1], ast[2], ast[3]
        obj_value = obj.get(field)
        
        if op == '=':
            return obj_value == value
        elif op == '!=':
            return obj_value != value
        elif op == '>':
            return obj_value > value
        elif op == '<':
            return obj_value < value
        elif op == '>=':
            return obj_value >= value
        elif op == '<=':
            return obj_value <= value
    
    return False

lines = sys.stdin.read().strip().split('\n')
filter_expr = lines[0]
json_objects = lines[1:]

tokens = tokenize(filter_expr)
ast = parse_expression(tokens)

for json_line in json_objects:
    obj = json.loads(json_line)
    if evaluate(ast, obj):
        print(json.dumps(obj, separators=(',', ':')))