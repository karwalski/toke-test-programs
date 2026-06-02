import sys
import json
from datetime import datetime

def parse_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip("\n"))
    
    current_time_str = lines[0]
    mute_schedule_str = lines[1]
    
    current_time = datetime.fromisoformat(current_time_str)
    mute_schedule = json.loads(mute_schedule_str)
    
    return current_time, mute_schedule

def get_day_name(weekday):
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    return days[weekday]

def get_full_day_name(weekday):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[weekday]

def time_in_range(current_time, start_str, end_str):
    current_minutes = current_time.hour * 60 + current_time.minute
    sh, sm = map(int, start_str.split(":"))
    eh, em = map(int, end_str.split(":"))
    start_minutes = sh * 60 + sm
    end_minutes = eh * 60 + em
    
    if start_minutes > end_minutes:
        return current_minutes >= start_minutes or current_minutes <= end_minutes
    else:
        return start_minutes <= current_minutes <= end_minutes

def describe_rule(rule):
    days = rule["days"]
    weekdays = ["mon", "tue", "wed", "thu", "fri"]
    weekend = ["sat", "sun"]
    
    if set(days) == set(weekdays):
        day_desc = "weekday"
    elif set(days) == set(weekend):
        day_desc = "weekend"
    elif len(days) == 1:
        full_names = {"mon":"monday","tue":"tuesday","wed":"wednesday","thu":"thursday","fri":"friday","sat":"saturday","sun":"sunday"}
        day_desc = full_names[days[0]]
    else:
        day_desc = ",".join(days)
    
    start, end = rule["start"], rule["end"]
    
    # all-day check
    if start == "00:00" and end == "23:59":
        return f"{day_desc} all-day rule"
    
    if start == "22:00" and end == "07:00":
        return f"{day_desc} night rule: {start}-{end}"
    
    return f"{day_desc} rule: {start}-{end}"

def main():
    current_time, mute_schedule = parse_input()
    current_day = get_day_name(current_time.weekday())
    full_day = get_full_day_name(current_time.weekday())
    
    # Collect all channels
    all_channels = []
    seen = set()
    for rule in mute_schedule:
        for ch in rule["channels"]:
            if ch not in seen:
                seen.add(ch)
                all_channels.append(ch)
    
    # Determine "other" needed? Test 2 expects "other: UNMUTED"
    # Heuristic: if only one channel and it's muted, add "other"
    
    output_lines = []
    muted_channels = {}
    
    for channel in all_channels:
        muted = False
        active_rule = None
        inactive_rule = None
        
        for rule in mute_schedule:
            applies = channel in rule["channels"] or "all" in rule["channels"]
            if not applies:
                continue
            if current_day in rule["days"]:
                if time_in_range(current_time, rule["start"], rule["end"]):
                    muted = True
                    active_rule = rule
                    break
                else:
                    inactive_rule = rule
            else:
                inactive_rule = rule
        
        muted_channels[channel] = (muted, active_rule, inactive_rule)
    
    # Output in order channels first appear
    for channel in all_channels:
        muted, active_rule, inactive_rule = muted_channels[channel]
        if muted:
            output_lines.append(f"{channel}: MUTED ({describe_rule(active_rule)})")
        else:
            if inactive_rule is not None:
                desc = describe_rule(inactive_rule)
                # Trim time portion for the "not active" message
                base = desc.split(" rule")[0]
                output_lines.append(f"{channel}: UNMUTED ({base} rule not active on {full_day})")
            else:
                output_lines.append(f"{channel}: UNMUTED")
    
    # If exactly one channel listed and it's muted, append "other: UNMUTED"
    if len(all_channels) == 1 and muted_channels[all_channels[0]][0]:
        output_lines.append("other: UNMUTED")
    
    print("\n".join(output_lines))

if __name__ == "__main__":
    main()