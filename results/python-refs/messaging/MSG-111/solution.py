import sys

# Emoji mapping dictionary
emoji_map = {
    ':thumbsup:': '👍',
    ':fire:': '🔥',
    ':heart:': '❤️',
    ':smile:': '😊',
    ':laugh:': '😂',
    ':cry:': '😢',
    ':angry:': '😠',
    ':wink:': '😉',
    ':kiss:': '😘',
    ':sunglasses:': '😎',
    ':party:': '🎉',
    ':rocket:': '🚀',
    ':star:': '⭐',
    ':check:': '✅',
    ':x:': '❌',
    ':warning:': '⚠️',
    ':info:': 'ℹ️',
    ':bulb:': '💡',
    ':money:': '💰',
    ':gift:': '🎁'
}

# Create reverse mapping for encoding
reverse_emoji_map = {v: k for k, v in emoji_map.items()}

def decode_emojis(text):
    """Convert shortcodes to emoji Unicode characters"""
    result = text
    for shortcode, emoji in emoji_map.items():
        result = result.replace(shortcode, emoji)
    return result

def encode_emojis(text):
    """Convert emoji Unicode characters to shortcodes"""
    result = text
    for emoji, shortcode in reverse_emoji_map.items():
        result = result.replace(emoji, shortcode)
    return result

# Read input
direction = input().strip()
text = input()

# Process based on direction
if direction == "decode":
    output = decode_emojis(text)
elif direction == "encode":
    output = encode_emojis(text)
else:
    output = text

print(output)