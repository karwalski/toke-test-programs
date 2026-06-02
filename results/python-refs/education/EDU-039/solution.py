def format_time(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

# Read input
line = input().strip()
work_min, break_min, total_min = map(int, line.split())

current_time = 0

while current_time < total_min:
    # Work block
    work_start = current_time
    work_end = min(current_time + work_min, total_min)
    print(f"{format_time(work_start)}-{format_time(work_end)} WORK")
    current_time = work_end
    
    # Break block (only if there's time left)
    if current_time < total_min:
        break_start = current_time
        break_end = min(current_time + break_min, total_min)
        print(f"{format_time(break_start)}-{format_time(break_end)} BREAK")
        current_time = break_end