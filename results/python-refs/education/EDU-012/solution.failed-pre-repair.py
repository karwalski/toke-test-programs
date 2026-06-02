import random

# Read the first line to get operation, count, and max value
first_line = input().strip().split()
op = first_line[0]
count = int(first_line[1])
max_val = int(first_line[2])

correct_answers = 0
total_problems = count

for i in range(count):
    # Generate two random numbers
    num1 = random.randint(1, max_val)
    num2 = random.randint(1, max_val)
    
    # Calculate the correct answer based on operation
    if op == 'add':
        correct_answer = num1 + num2
        print(f"{num1} + {num2} = ?")
    elif op == 'sub':
        correct_answer = num1 - num2
        print(f"{num1} - {num2} = ?")
    elif op == 'mul':
        correct_answer = num1 * num2
        print(f"{num1} * {num2} = ?")
    elif op == 'div':
        correct_answer = num1 // num2
        print(f"{num1} / {num2} = ?")
    
    # Read user's answer
    user_answer = int(input().strip())
    
    # Check if answer is correct
    if user_answer == correct_answer:
        print("Correct")
        correct_answers += 1
    else:
        print("Incorrect")

# Calculate and display score
percentage = (correct_answers / total_problems) * 100
print(f"Score: {correct_answers}/{total_problems} ({percentage:.0f}%)")