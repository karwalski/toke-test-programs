# Read input
answer_key = input().strip().split(',')
student_answers = input().strip().split(',')

# Grade each question
correct_count = 0
for i in range(len(answer_key)):
    if answer_key[i] == student_answers[i]:
        print(f"Q{i+1}: Correct")
        correct_count += 1
    else:
        print(f"Q{i+1}: Incorrect")

# Calculate and print score
total_questions = len(answer_key)
percentage = int((correct_count / total_questions) * 100)
print(f"Score: {correct_count}/{total_questions} ({percentage}%)")