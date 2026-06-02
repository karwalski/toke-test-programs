import json
import re
import sys
from datetime import datetime

def normalize_slack_message(msg):
    # Convert timestamp
    ts = float(msg["ts"])
    timestamp = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Extract mentions and links from text
    text = msg["text"]
    mentions = []
    links = []
    
    # Find mentions <@USER_ID>
    mention_pattern = r'<@([^>]+)>'
    mentions = re.findall(mention_pattern, text)
    
    # Find links <URL|text> or <URL>
    link_pattern = r'<(https?://[^|>]+)(?:\|[^>]*)?>'
    links = re.findall(link_pattern, text)
    
    # Clean text - replace mentions and links
    clean_text = re.sub(r'<@([^>]+)>', r'@\1', text)
    clean_text = re.sub(r'<(https?://[^|>]+)\|([^>]*)>', r'\2', clean_text)
    clean_text = re.sub(r'<(https?://[^>]+)>', r'\1', clean_text)
    
    return {
        "timestamp": timestamp,
        "sender": msg["user"],
        "text": clean_text,
        "channel": msg["channel"],
        "links": links,
        "mentions": mentions,
        "source": "slack"
    }

def normalize_discord_message(msg):
    # Discord timestamp is typically in ISO format or timestamp
    if "timestamp" in msg:
        timestamp = msg["timestamp"]
        if not timestamp.endswith('Z'):
            # Convert from timestamp if needed
            ts = float(timestamp)
            timestamp = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    text = msg.get("content", "")
    mentions = []
    links = []
    
    # Discord mentions <@!USER_ID> or <@USER_ID>
    mention_pattern = r'<@!?([^>]+)>'
    mentions = re.findall(mention_pattern, text)
    
    # Find links
    link_pattern = r'(https?://[^\s]+)'
    links = re.findall(link_pattern, text)
    
    # Clean text
    clean_text = re.sub(r'<@!?([^>]+)>', r'@\1', text)
    
    return {
        "timestamp": timestamp,
        "sender": msg.get("author", {}).get("id", msg.get("user", "")),
        "text": clean_text,
        "channel": msg.get("channel_id", msg.get("channel", "")),
        "links": links,
        "mentions": mentions,
        "source": "discord"
    }

def normalize_teams_message(msg):
    # Teams timestamp handling
    timestamp = msg.get("createdDateTime", "")
    if not timestamp.endswith('Z'):
        if timestamp:
            # Convert from timestamp if needed
            try:
                ts = float(timestamp)
                timestamp = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")
            except:
                timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    text = msg.get("body", {}).get("content", "") if isinstance(msg.get("body"), dict) else msg.get("text", "")
    mentions = []
    links = []
    
    # Teams mentions
    mention_pattern = r'<at>([^<]+)</at>'
    mentions = re.findall(mention_pattern, text)
    
    # Find links
    link_pattern = r'(https?://[^\s]+)'
    links = re.findall(link_pattern, text)
    
    # Clean text
    clean_text = re.sub(r'<at>([^<]+)</at>', r'@\1', text)
    
    return {
        "timestamp": timestamp,
        "sender": msg.get("from", {}).get("user", {}).get("id", "") if isinstance(msg.get("from"), dict) else msg.get("user", ""),
        "text": clean_text,
        "channel": msg.get("channelIdentity", {}).get("channelId", "") if isinstance(msg.get("channelIdentity"), dict) else msg.get("channel", ""),
        "links": links,
        "mentions": mentions,
        "source": "teams"
    }

# Read input
platform = input().strip()
message_json = input().strip()

# Parse message
message = json.loads(message_json)

# Normalize based on platform
if platform == "slack":
    normalized = normalize_slack_message(message)
elif platform == "discord":
    normalized = normalize_discord_message(message)
elif platform == "teams":
    normalized = normalize_teams_message(message)
else:
    normalized = {}

# Output normalized message
print(json.dumps(normalized, separators=(',', ':')))