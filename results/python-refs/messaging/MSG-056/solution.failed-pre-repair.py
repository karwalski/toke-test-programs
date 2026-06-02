import sys
from collections import defaultdict

def find_common_phrases(messages, min_length):
    # Find all possible phrases of at least min_length
    phrase_count = defaultdict(int)
    phrase_positions = defaultdict(list)
    
    for msg_idx, message in enumerate(messages):
        words = message.split()
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                phrase = ' '.join(words[i:j])
                if len(phrase) >= min_length:
                    phrase_count[phrase] += 1
                    phrase_positions[phrase].append((msg_idx, i, j))
    
    # Find phrases that appear in multiple messages and would save space
    dictionary = {}
    dict_counter = 1
    
    # Sort by length (longer first) to prioritize longer matches
    candidates = [(phrase, count) for phrase, count in phrase_count.items() if count > 1]
    candidates.sort(key=lambda x: len(x[0]), reverse=True)
    
    used_positions = set()
    
    for phrase, count in candidates:
        # Check if this phrase would save space
        dict_entry_cost = len(phrase)
        replacement_cost = len(f"{{D{dict_counter}}}")
        savings = (dict_entry_cost - replacement_cost) * count - dict_entry_cost
        
        if savings > 0:
            # Check if positions are available (not overlapping with already used)
            positions = phrase_positions[phrase]
            available_positions = []
            
            for msg_idx, start, end in positions:
                position_range = set(range(start, end))
                msg_used = {pos for pos in used_positions if pos[0] == msg_idx}
                word_positions_used = {pos[1] for pos in msg_used}
                
                if not any(pos in word_positions_used for pos in position_range):
                    available_positions.append((msg_idx, start, end))
            
            if len(available_positions) > 1:
                # Add to dictionary
                dictionary[f"D{dict_counter}"] = phrase
                
                # Mark positions as used
                for msg_idx, start, end in available_positions:
                    for pos in range(start, end):
                        used_positions.add((msg_idx, pos))
                
                dict_counter += 1
    
    return dictionary

def compress_messages(messages, dictionary):
    compressed = []
    
    for message in messages:
        compressed_msg = message
        
        # Sort dictionary items by length (longer first) to avoid partial replacements
        dict_items = sorted(dictionary.items(), key=lambda x: len(x[1]), reverse=True)
        
        for dict_key, phrase in dict_items:
            compressed_msg = compressed_msg.replace(phrase, f"{{{dict_key}}}")
        
        compressed.append(compressed_msg)
    
    return compressed

def calculate_savings(original_messages, dictionary, compressed_messages):
    original_length = sum(len(msg) for msg in original_messages)
    
    # Dictionary overhead
    dict_length = sum(len(phrase) for phrase in dictionary.values())
    
    # Compressed messages length
    compressed_length = sum(len(msg) for msg in compressed_messages)
    
    total_compressed = dict_length + compressed_length
    
    if original_length == 0:
        return 0
    
    savings_percent = round((original_length - total_compressed) / original_length * 100)
    return max(0, savings_percent)

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    min_length = int(lines[0])
    messages = lines[1:]
    
    # Find common phrases
    dictionary = find_common_phrases(messages, min_length)
    
    # Compress messages
    compressed_messages = compress_messages(messages, dictionary)
    
    # Calculate savings
    savings = calculate_savings(messages, dictionary, compressed_messages)
    
    # Output
    print("DICT:")
    for key in sorted(dictionary.keys(), key=lambda x: int(x[1:])):
        print(f"  {key}={dictionary[key]}")
    
    print("COMPRESSED:")
    for msg in compressed_messages:
        print(f"  {msg}")
    
    print(f"Savings: {savings}%")

if __name__ == "__main__":
    main()