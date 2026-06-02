import sys
from datetime import datetime, timedelta

def parse_timestamp(timestamp_str):
    return datetime.fromisoformat(timestamp_str)

def format_time(dt):
    return dt.strftime("%H:%M")

def main():
    lines = [line.strip() for line in sys.stdin.readlines()]
    timeout_minutes = int(lines[0])
    
    user_sessions = {}
    
    for line in lines[1:]:
        if not line:
            continue
            
        parts = line.split(' ', 2)
        user_id = parts[0]
        timestamp = parse_timestamp(parts[1])
        event = parts[2]
        
        if user_id not in user_sessions:
            user_sessions[user_id] = []
        
        # Check if this event belongs to an existing session or starts a new one
        sessions = user_sessions[user_id]
        
        if not sessions:
            # First session for this user
            sessions.append({
                'start': timestamp,
                'end': timestamp,
                'events': 1
            })
        else:
            last_session = sessions[-1]
            time_diff = timestamp - last_session['end']
            
            if time_diff <= timedelta(minutes=timeout_minutes):
                # Extend existing session
                last_session['end'] = timestamp
                last_session['events'] += 1
            else:
                # Start new session
                sessions.append({
                    'start': timestamp,
                    'end': timestamp,
                    'events': 1
                })
    
    # Output sessions
    for user_id in sorted(user_sessions.keys()):
        sessions = user_sessions[user_id]
        for i, session in enumerate(sessions, 1):
            start_time = format_time(session['start'])
            end_time = format_time(session['end'])
            event_count = session['events']
            print(f"Session {user_id} {i}: {start_time}-{end_time} ({event_count} events)")

if __name__ == "__main__":
    main()