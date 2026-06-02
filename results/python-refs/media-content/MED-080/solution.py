import sys
import re

# Emoji mapping dictionary
emoji_map = {
    'smile': '😄',
    'thumbsup': '👍',
    'heart': '❤️',
    'fire': '🔥',
    'star': '⭐',
    'rocket': '🚀',
    'party': '🎉',
    'clap': '👏',
    'ok_hand': '👌',
    'thumbsdown': '👎',
    'cry': '😢',
    'laugh': '😂',
    'wink': '😉',
    'cool': '😎',
    'thinking': '🤔',
    'shrug': '🤷',
    'wave': '👋',
    'point_right': '👉',
    'point_left': '👈',
    'point_up': '👆',
    'point_down': '👇',
    'muscle': '💪',
    'pray': '🙏',
    'eyes': '👀',
    'raised_hands': '🙌'
}

def replace_emoji(match):
    shortcode = match.group(1)
    return emoji_map.get(shortcode, match.group(0))

# Read input from stdin
text = sys.stdin.read().strip()

# Replace shortcodes with emoji
result = re.sub(r':(\w+):', replace_emoji, text)

# Write to stdout
print(result)