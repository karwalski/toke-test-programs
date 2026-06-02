def fibonacci_up_to(n):
    """Generate Fibonacci numbers up to n"""
    fibs = []
    a, b = 1, 1
    while a <= n:
        fibs.append(a)
        a, b = b, a + b
    return fibs

def is_losing_position(stones, fibs, memo):
    """Check if a position is losing using memoization"""
    if stones in memo:
        return memo[stones]
    
    if stones == 0:
        memo[stones] = True
        return True
    
    # Try all possible Fibonacci moves
    for fib in fibs:
        if fib > stones:
            break
        # If taking 'fib' stones leads to a losing position for opponent,
        # then current position is winning
        if is_losing_position(stones - fib, fibs, memo):
            memo[stones] = False
            return False
    
    # All moves lead to winning positions for opponent, so this is losing
    memo[stones] = True
    return True

def find_optimal_move(stones):
    """Find the optimal move in Fibonacci Nim"""
    if stones == 0:
        return "Losing position"
    
    fibs = fibonacci_up_to(stones)
    memo = {}
    
    # If current position is already losing, return that
    if is_losing_position(stones, fibs, memo):
        return "Losing position"
    
    # Find a move that leads to a losing position for opponent
    for fib in fibs:
        if fib > stones:
            break
        if is_losing_position(stones - fib, fibs, memo):
            return str(fib)
    
    return "Losing position"

# Read input
stones = int(input().strip())

# Find and print optimal move
result = find_optimal_move(stones)
print(result)