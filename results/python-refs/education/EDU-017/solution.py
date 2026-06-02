total_minutes, num_sections = map(int, input().split())

sections = []
for _ in range(num_sections):
    sections.append(input().strip())

duration_per_section = total_minutes // num_sections

for i in range(num_sections):
    start_minutes = i * duration_per_section
    end_minutes = (i + 1) * duration_per_section
    
    start_hours = start_minutes // 60
    start_mins = start_minutes % 60
    end_hours = end_minutes // 60
    end_mins = end_minutes % 60
    
    start_time = f"{start_hours:02d}:{start_mins:02d}"
    end_time = f"{end_hours:02d}:{end_mins:02d}"
    
    print(f"Section {i+1}: {sections[i]} | start {start_time} | end {end_time} | duration {duration_per_section}min")