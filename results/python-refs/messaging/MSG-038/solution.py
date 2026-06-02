import json
import sys
import re

def tokenize_query(query):
    tokens = []
    i = 0
    while i < len(query):
        if query[i].isspace():
            i += 1
        elif query[i] == '(':
            tokens.append('(')
            i += 1
        elif query[i] == ')':
            tokens.append(')')
            i += 1
        elif query[i:i+3].upper() == 'AND':
            tokens.append('AND')
            i += 3
        elif query[i:i+2].upper() == 'OR':
            tokens.append('OR')
            i += 2
        elif query[i:i+3].upper() == 'NOT':
            tokens.append('NOT')
            i += 3
        else:
            # Read word
            word = ''
            while i < len(query) and not query[i].isspace() and query[i] not in '()':
                word += query[i]
                i += 1
            if word:
                tokens.append(word)
    return tokens

def parse_expression(tokens, pos):
    return parse_or(tokens, pos)

def parse_or(tokens, pos):
    left, pos = parse_and(tokens, pos)
    
    while pos < len(tokens) and tokens[pos] == 'OR':
        pos += 1  # skip 'OR'
        right, pos = parse_and(tokens, pos)
        left = ('OR', left, right)
    
    return left, pos

def parse_and(tokens, pos):
    left, pos = parse_not(tokens, pos)
    
    while pos < len(tokens) and tokens[pos] == 'AND':
        pos += 1  # skip 'AND'
        right, pos = parse_not(tokens, pos)
        left = ('AND', left, right)
    
    return left, pos

def parse_not(tokens, pos):
    if pos < len(tokens) and tokens[pos] == 'NOT':
        pos += 1  # skip 'NOT'
        expr, pos = parse_primary(tokens, pos)
        return ('NOT', expr), pos
    else:
        return parse_primary(tokens, pos)

def parse_primary(tokens, pos):
    if pos < len(tokens) and tokens[pos] == '(':
        pos += 1  # skip '('
        expr, pos = parse_expression(tokens, pos)
        if pos < len(tokens) and tokens[pos] == ')':
            pos += 1  # skip ')'
        return expr, pos
    elif pos < len(tokens):
        word = tokens[pos]
        pos += 1
        return word, pos
    else:
        return None, pos

def evaluate(ast, text):
    if isinstance(ast, str):
        return ast.lower() in text.lower()
    elif ast[0] == 'AND':
        return evaluate(ast[1], text) and evaluate(ast[2], text)
    elif ast[0] == 'OR':
        return evaluate(ast[1], text) or evaluate(ast[2], text)
    elif ast[0] == 'NOT':
        return not evaluate(ast[1], text)
    return False

def main():
    query = input().strip()
    messages_json = input().strip()
    
    messages = json.loads(messages_json)
    
    tokens = tokenize_query(query)
    if not tokens:
        return
    
    ast, _ = parse_expression(tokens, 0)
    
    matching_ids = []
    for message in messages:
        if evaluate(ast, message['text']):
            matching_ids.append(message['id'])
    
    for msg_id in matching_ids:
        print(msg_id)

if __name__ == "__main__":
    main()