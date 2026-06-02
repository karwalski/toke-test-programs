work_minutes, break_minutes, num_pomodoros = map(int, input().split())

for i in range(1, num_pomodoros + 1):
    print(f"Pomodoro {i}: work {work_minutes}min | break {break_minutes}min")

total_focused_time = work_minutes * num_pomodoros
print(f"Total focused time: {total_focused_time}min")