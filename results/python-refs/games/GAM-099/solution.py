from itertools import permutations

def solve_cryptarithmetic(equation):
    # Parse the equation
    parts = equation.replace('=', '+').split('+')
    parts = [part.strip() for part in parts]
    
    # The result is the last part, operands are the rest
    operands = parts[:-1]
    result = parts[-1]
    
    # Get all unique letters
    letters = set()
    for word in parts:
        letters.update(word)
    letters = sorted(list(letters))
    
    # Get first letters (cannot be 0)
    first_letters = set()
    for word in parts:
        if word:
            first_letters.add(word[0])
    
    # Try all possible digit assignments
    for perm in permutations(range(10), len(letters)):
        mapping = dict(zip(letters, perm))
        
        # Check if any first letter is assigned 0
        if any(mapping[letter] == 0 for letter in first_letters):
            continue
        
        # Convert words to numbers using the mapping
        numbers = []
        valid = True
        
        for word in parts:
            num = 0
            for char in word:
                num = num * 10 + mapping[char]
            numbers.append(num)
        
        # Check if the equation holds
        if sum(numbers[:-1]) == numbers[-1]:
            # Found a solution
            result_parts = []
            for letter in sorted(letters):
                result_parts.append(f"{letter}={mapping[letter]}")
            
            solution_line = " ".join(result_parts)
            
            # Create verification line
            operand_strs = []
            for i, word in enumerate(operands):
                operand_strs.append(str(numbers[i]))
            
            verification_line = " + ".join(operand_strs) + " = " + str(numbers[-1])
            
            return solution_line + "\n" + verification_line
    
    return "No solution"

# Read input
equation = input().strip()
print(solve_cryptarithmetic(equation))