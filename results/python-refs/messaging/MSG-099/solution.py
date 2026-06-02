import json
import sys

# Read input
current_user = input().strip()
read_positions = json.loads(input().strip())
messages = json.loads(input().strip())

# Calculate unread counts per channel
channel_stats = {}

for message in messages:
    channel = message["channel"]
    message_id = int(message["id"])
    mentions = message["mentions"]
    
    # Check if message is unread
    last_read_id = int(read_positions.get(channel, "0"))
    if message_id > last_read_id:
        # Initialize channel stats if not exists
        if channel not in channel_stats:
            channel_stats[channel] = {"unread": 0, "mentions": 0}
        
        # Increment unread count
        channel_stats[channel]["unread"] += 1
        
        # Check if current user is mentioned
        if current_user in mentions:
            channel_stats[channel]["mentions"] += 1

# Calculate totals
total_unread = sum(stats["unread"] for stats in channel_stats.values())
total_mentions = sum(stats["mentions"] for stats in channel_stats.values())

# Output per-channel stats
for channel in sorted(channel_stats.keys()):
    stats = channel_stats[channel]
    print(f"{channel}: {stats['unread']} unread ({stats['mentions']} mention)")

# Output totals
print(f"total: {total_unread} unread ({total_mentions} mentions)")