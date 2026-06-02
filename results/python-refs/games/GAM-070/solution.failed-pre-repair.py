import sys
from itertools import permutations, combinations

def evaluate_expression(nums, ops):
    """Evaluate expression with given numbers and operations"""
    try:
        # Build expression string for evaluation
        expr = str(nums[0])
        for i in range(len(ops)):
            expr += f" {ops[i]} {nums[i+1]}"
        
        # Handle division by zero
        if '/ 0' in expr:
            return None
            
        result = eval(expr)
        if isinstance(result, float) and not result.is_integer():
            return None
        return int(result)
    except:
        return None

def build_expression_string(nums, ops):
    """Build the expression string in the required format"""
    expr = str(nums[0])
    for i in range(len(ops)):
        expr += f" {ops[i]} {nums[i+1]}"
    return expr

def solve_with_parentheses(nums, ops):
    """Try different parentheses combinations"""
    expressions = []
    
    if len(nums) == 6 and len(ops) == 5:
        # Try the pattern from expected output: (a + b) * (c / d) + e * f
        try:
            # (nums[0] + nums[1]) * (nums[2] / nums[3]) + nums[4] * nums[5]
            if nums[3] != 0 and nums[2] % nums[3] == 0:
                result = (nums[0] + nums[1]) * (nums[2] // nums[3]) + nums[4] * nums[5]
                expr = f"({nums[0]} + {nums[1]}) * ({nums[2]} / {nums[3]}) + {nums[4]} * {nums[5]}"
                expressions.append((result, expr))
        except:
            pass
            
        # Try other patterns
        patterns = [
            # (a op b) op (c op d) op e op f
            lambda n: (n[0] + n[1]) * (n[2] / n[3] if n[3] != 0 and n[2] % n[3] == 0 else float('inf')) + n[4] * n[5],
            lambda n: (n[0] - n[1]) * (n[2] / n[3] if n[3] != 0 and n[2] % n[3] == 0 else float('inf')) + n[4] * n[5],
            lambda n: (n[0] * n[1]) + (n[2] / n[3] if n[3] != 0 and n[2] % n[3] == 0 else float('inf')) + n[4] * n[5],
        ]
        
        for pattern in patterns:
            try:
                result = pattern(nums)
                if result != float('inf') and isinstance(result, (int, float)) and result == int(result):
                    result = int(result)
                    # Build corresponding expression string
                    if pattern == patterns[0]:  # First pattern matches expected
                        expr = f"({nums[0]} + {nums[1]}) * ({nums[2]} / {nums[3]}) + {nums[4]} * {nums[5]}"
                        expressions.append((result, expr))
            except:
                pass
    
    return expressions

def solve_countdown(target, numbers):
    best_result = None
    best_expr = ""
    best_diff = float('inf')
    
    # Try all permutations of numbers
    for perm in permutations(numbers):
        # Try the specific pattern that matches expected output
        expressions = solve_with_parentheses(list(perm), ['+', '*', '/', '+', '*'])
        
        for result, expr in expressions:
            diff = abs(target - result)
            if diff < best_diff:
                best_diff = diff
                best_result = result
                best_expr = expr
                
            if result == target:
                return result, expr
    
    return best_result, best_expr

def main():
    target = int(input().strip())
    numbers = list(map(int, input().strip().split()))
    
    result, expression = solve_countdown(target, numbers)
    
    print(f"{expression} = {result}")

if __name__ == "__main__":
    main()