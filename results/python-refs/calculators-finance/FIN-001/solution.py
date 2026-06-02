def evaluate_rpn(tokens):
    stack = []
    
    for token in tokens:
        if token in ['+', '-', '*', '/']:
            # Pop two operands
            b = stack.pop()
            a = stack.pop()
            
            # Perform operation
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b
            
            stack.append(result)
        else:
            # It's a number, convert to appropriate type
            if '.' in token:
                stack.append(float(token))
            else:
                stack.append(int(token))
    
    return stack[0]

# Read input and process
expression = input().strip()
tokens = expression.split()
result = evaluate_rpn(tokens)

# Output result
if isinstance(result, float) and result.is_integer():
    print(int(result))
else:
    print(result)