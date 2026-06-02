import math
import sys

def calculator():
    line = input().strip()
    parts = line.split()
    
    if len(parts) < 2:
        return
    
    func = parts[0]
    
    if func in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt']:
        arg = float(parts[1])
        
        if func == 'sin':
            result = math.sin(arg)
        elif func == 'cos':
            result = math.cos(arg)
        elif func == 'tan':
            result = math.tan(arg)
        elif func == 'log':
            result = math.log10(arg)
        elif func == 'ln':
            result = math.log(arg)
        elif func == 'sqrt':
            result = math.sqrt(arg)
            
    elif func == 'pow' and len(parts) >= 3:
        base = float(parts[1])
        exponent = float(parts[2])
        result = math.pow(base, exponent)
    
    print(f"{result:.6f}")

calculator()