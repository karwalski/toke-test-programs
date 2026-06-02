import itertools

def evaluate_expression(nums, ops, structure):
    """Evaluate expression based on numbers, operations, and structure"""
    try:
        a, b, c, d = nums
        op1, op2, op3 = ops
        
        # Define operation functions
        def apply_op(x, y, op):
            if op == '+':
                return x + y
            elif op == '-':
                return x - y
            elif op == '*':
                return x * y
            elif op == '/':
                return x / y if y != 0 else float('inf')
        
        # Different parenthesization structures
        if structure == 1:  # ((a op b) op c) op d
            temp1 = apply_op(a, b, op1)
            temp2 = apply_op(temp1, c, op2)
            result = apply_op(temp2, d, op3)
        elif structure == 2:  # (a op (b op c)) op d
            temp1 = apply_op(b, c, op2)
            temp2 = apply_op(a, temp1, op1)
            result = apply_op(temp2, d, op3)
        elif structure == 3:  # a op ((b op c) op d)
            temp1 = apply_op(b, c, op2)
            temp2 = apply_op(temp1, d, op3)
            result = apply_op(a, temp2, op1)
        elif structure == 4:  # a op (b op (c op d))
            temp1 = apply_op(c, d, op3)
            temp2 = apply_op(b, temp1, op2)
            result = apply_op(a, temp2, op1)
        elif structure == 5:  # (a op b) op (c op d)
            temp1 = apply_op(a, b, op1)
            temp2 = apply_op(c, d, op3)
            result = apply_op(temp1, temp2, op2)
        
        return result
    except:
        return float('inf')

def format_expression(nums, ops, structure):
    """Format the expression string with proper parentheses"""
    a, b, c, d = nums
    op1, op2, op3 = ops
    
    if structure == 1:  # ((a op b) op c) op d
        return f"(({a} {op1} {b}) {op2} {c}) {op3} {d}"
    elif structure == 2:  # (a op (b op c)) op d
        return f"({a} {op1} ({b} {op2} {c})) {op3} {d}"
    elif structure == 3:  # a op ((b op c) op d)
        return f"{a} {op1} (({b} {op2} {c}) {op3} {d})"
    elif structure == 4:  # a op (b op (c op d))
        return f"{a} {op1} ({b} {op2} ({c} {op3} {d}))"
    elif structure == 5:  # (a op b) op (c op d)
        return f"({a} {op1} {b}) {op2} ({c} {op3} {d})"

def solve_24(numbers):
    """Find an expression that equals 24"""
    operations = ['+', '-', '*', '/']
    
    # Try all permutations of numbers
    for nums in itertools.permutations(numbers):
        # Try all combinations of operations
        for ops in itertools.product(operations, repeat=3):
            # Try all parenthesization structures
            for structure in range(1, 6):
                result = evaluate_expression(nums, ops, structure)
                if abs(result - 24) < 1e-9:
                    return format_expression(nums, ops, structure)
    
    return "Impossible"

# Read input
numbers = list(map(int, input().split()))

# Solve and print result
result = solve_24(numbers)
print(result)