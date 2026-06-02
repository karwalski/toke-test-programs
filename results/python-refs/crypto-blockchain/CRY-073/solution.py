def execute_vm(instructions):
    stack = []
    i = 0
    
    while i < len(instructions):
        op = instructions[i]
        
        if op == "PUSH":
            i += 1
            value = int(instructions[i])
            stack.append(value)
        elif op == "ADD":
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif op == "SUB":
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif op == "MUL":
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        elif op == "DUP":
            stack.append(stack[-1])
        elif op == "SWAP":
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif op == "POP":
            stack.pop()
        
        i += 1
    
    return stack

# Read input and parse instructions
input_line = input().strip()
instructions = input_line.split()

# Execute the virtual machine
final_stack = execute_vm(instructions)

# Output the stack (top to bottom)
if final_stack:
    print(' '.join(map(str, reversed(final_stack))))