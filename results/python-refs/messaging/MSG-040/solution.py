import json
import sys
from datetime import datetime, time

def parse_time(time_str):
    """Parse time string in HH:MM format to time object"""
    return datetime.strptime(time_str, "%H:%M").time()

def is_in_quiet_hours(current_time_str, quiet_hours_str):
    """Check if current time is within quiet hours"""
    if not quiet_hours_str:
        return False
    
    current_time = parse_time(current_time_str)
    start_str, end_str = quiet_hours_str.split('-')
    start_time = parse_time(start_str)
    end_time = parse_time(end_str)
    
    # Handle overnight quiet hours (e.g., 22:00-08:00)
    if start_time > end_time:
        return current_time >= start_time or current_time <= end_time
    else:
        return start_time <= current_time <= end_time

def main():
    # Read input
    user_prefs_line = input().strip()
    message_line = input().strip()
    
    # Parse JSON
    user_prefs = json.loads(user_prefs_line)
    message = json.loads(message_line)
    
    # Extract data
    channels = user_prefs.get("channels", {})
    quiet_hours = user_prefs.get("quiet_hours", "")
    priority_override = user_prefs.get("priority_override", 0)
    
    message_priority = message.get("priority", 0)
    message_time = message.get("time", "")
    
    # Check if message should be suppressed due to quiet hours
    if quiet_hours and is_in_quiet_hours(message_time, quiet_hours):
        if message_priority < priority_override:
            print(f"SUPPRESSED (quiet hours, priority {message_priority} < override {priority_override})")
            return
    
    # Get enabled channels
    enabled_channels = []
    for channel, enabled in channels.items():
        if enabled:
            enabled_channels.append(channel)
    
    # Output channels
    if enabled_channels:
        print(enabled_channels)
    else:
        print("[]")

if __name__ == "__main__":
    main()