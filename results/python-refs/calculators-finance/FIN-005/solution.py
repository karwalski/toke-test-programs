def multiply_strings(num1, num2):
    if num1 == "0" or num2 == "0":
        return "0"
    
    # Initialize result array
    result = [0] * (len(num1) + len(num2))
    
    # Reverse both numbers to make multiplication easier
    num1 = num1[::-1]
    num2 = num2[::-1]
    
    # Multiply each digit
    for i in range(len(num1)):
        for j in range(len(num2)):
            # Convert characters to integers
            digit1 = int(num1[i])
            digit2 = int(num2[j])
            
            # Multiply digits and add to result
            product = digit1 * digit2
            result[i + j] += product
            
            # Handle carry
            if result[i + j] >= 10:
                result[i + j + 1] += result[i + j] // 10
                result[i + j] %= 10
    
    # Convert result array to string, removing leading zeros
    result_str = ""
    leading_zero = True
    
    for i in range(len(result) - 1, -1, -1):
        if result[i] != 0:
            leading_zero = False
        if not leading_zero:
            result_str += str(result[i])
    
    return result_str if result_str else "0"

# Read input
num1 = input().strip()
num2 = input().strip()

# Calculate and print result
print(multiply_strings(num1, num2))