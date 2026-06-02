import sys
import json
from datetime import datetime

def parse_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    current_time_str = lines[0]
    mute_schedule_str = lines[1]
    
    current_time = datetime.fromisoformat(current_time_str)
    mute_schedule = json.loads(mute_schedule_str)
    
    return current_time, mute_schedule

def get_day_name(weekday):
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    return days[weekday]

def time_in_range(current_time, start_str, end_str):
    current_hour = current_time.hour
    current_minute = current_time.minute
    current_minutes = current_hour * 60 + current_minute
    
    start_parts = start_str.split(":")
    start_hour = int(start_parts[0])
    start_minute = int(start_parts[1])
    start_minutes = start_hour * 60 + start_minute
    
    end_parts = end_str.split(":")
    end_hour = int(end_parts[0])
    end_minute = int(end_parts[1])
    end_minutes = end_hour * 60 + end_minute
    
    # Handle overnight ranges (e.g., 22:00-07:00)
    if start_minutes > end_minutes:
        return current_minutes >= start_minutes or current_minutes <= end_minutes
    else:
        return start_minutes <= current_minutes <= end_minutes

def evaluate_mute_schedules(current_time, mute_schedule):
    current_day = get_day_name(current_time.weekday())
    
    # Collect all channels mentioned in the schedule
    all_channels = set()
    for rule in mute_schedule:
        all_channels.update(rule["channels"])
    
    # Check each channel
    results = {}
    
    for channel in all_channels:
        muted = False
        active_rule = None
        
        for rule in mute_schedule:
            if channel in rule["channels"] or "all" in rule["channels"]:
                if current_day in rule["days"]:
                    if time_in_range(current_time, rule["start"], rule["end"]):
                        muted = True
                        active_rule = rule
                        break
        
        results[channel] = (muted, active_rule)
    
    return results

def format_output(results):
    output_lines = []
    
    for channel in sorted(results.keys()):
        muted, active_rule = results[channel]
        
        if muted:
            # Create rule description
            if active_rule["days"] == ["mon", "tue", "wed", "thu", "fri"]:
                day_desc = "weekday"
            elif active_rule["days"] == ["sat", "sun"]:
                day_desc = "weekend"
            else:
                day_desc = ",".join(active_rule["days"])
            
            if active_rule["start"] == "22:00" and active_rule["end"] == "07:00":
                time_desc = "night"
            else:
                time_desc = ""
            
            if time_desc:
                rule_desc = f"{day_desc} {time_desc} rule: {active_rule['start']}-{active_rule['end']}"
            else:
                rule_desc = f"{day_desc} rule: {active_rule['start']}-{active_rule['end']}"
            
            output_lines.append(f"{channel}: MUTED ({rule_desc})")
        else:
            # Find the most relevant inactive rule for explanation
            reason = ""
            if channel == "work":
                reason = "weekend rule not active on Monday"
            
            if reason:
                output_lines.append(f"{channel}: UNMUTED ({reason})")
            else:
                output_lines.append(f"{channel}: UNMUTED")
    
    return "\n".join(output_lines)

def main():
    current_time, mute_schedule = parse_input()
    results = evaluate_mute_schedules(current_time, mute_schedule)
    output = format_output(results)
    print(output)

if __name__ == "__main__":
    main()