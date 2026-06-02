import json
import sys

def main():
    # Emoji shortcode to Unicode mapping
    emoji_map = {
        'thumbsup': '\U0001F44D',
        'heart': '\u2764',
        'fire': '\U0001F525',
        'smile': '\U0001F642',
        'cry': '\U0001F622',
        'angry': '\U0001F621',
        'laugh': '\U0001F602',
        'love': '\U0001F970',
        'sad': '\U0001F614',
        'wow': '\U0001F62E'
    }
    
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    reactions = json.loads(input_data)
    
    # Count emoji frequencies
    emoji_counts = {}
    
    for reaction in reactions:
        emoji = reaction['emoji']
        
        # Convert shortcode to Unicode if needed
        if emoji in emoji_map:
            unicode_emoji = emoji_map[emoji]
            shortcode = emoji
        else:
            # Assume it's already Unicode
            unicode_emoji = emoji
            # Find shortcode by reverse lookup
            shortcode = None
            for sc, uc in emoji_map.items():
                if uc == emoji:
                    shortcode = sc
                    break
            if shortcode is None:
                shortcode = emoji
        
        if shortcode not in emoji_counts:
            emoji_counts[shortcode] = {'unicode': unicode_emoji, 'count': 0}
        emoji_counts[shortcode]['count'] += 1
    
    # Sort by frequency (descending) then by name for ties
    sorted_emojis = sorted(emoji_counts.items(), 
                          key=lambda x: (-x[1]['count'], x[0]))
    
    # Generate output
    total_reactions = sum(data['count'] for data in emoji_counts.values())
    unique_count = len(emoji_counts)
    
    for shortcode, data in sorted_emojis:
        unicode_char = data['unicode']
        count = data['count']
        
        # Get Unicode code point in U+ format
        code_point = f"U+{ord(unicode_char):04X}"
        
        print(f"{shortcode} ({code_point}): {count}")
    
    print(f"total: {total_reactions}, unique: {unique_count}")

if __name__ == "__main__":
    main()