current_difficulty = int(input())
target_time = int(input())
actual_time = int(input())

new_difficulty = int(current_difficulty * target_time / actual_time)
print(new_difficulty)