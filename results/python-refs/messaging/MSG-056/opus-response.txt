import sys
from collections import defaultdict

def find_common_phrases(messages, min_length):
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
    
    dictionary = {}
    dict_counter = 1
    
    candidates = [(phrase, count) for phrase, count in phrase_count.items() if count > 1]
    candidates.sort(key=lambda x: (-len(x[0]), x[0]))
    
    used_positions = set()
    
    for phrase, count in candidates:
        positions = phrase_positions[phrase]
        available_positions = []
        
        for msg_idx, start, end in positions:
            overlap = False
            for pos in range(start, end):
                if (msg_idx, pos) in used_positions:
                    overlap = True
                    break
            if not overlap:
                available_positions.append((msg_idx, start, end))
        
        if len(available_positions) >= 2:
            dictionary[f"D{dict_counter}"] = phrase
            for msg_idx, start, end in available_positions:
                for pos in range(start, end):
                    used_positions.add((msg_idx, pos))
            dict_counter += 1
    
    return dictionary

def compress_messages(messages, dictionary):
    compressed = []
    for message in messages:
        words = message.split()
        # Try to match dictionary entries greedily, longest first
        dict_items = sorted(dictionary.items(), key=lambda x: -len(x[1].split()))
        
        result_parts = []
        i = 0
        while i < len(words):
            matched = False
            for dict_key, phrase in dict_items:
                phrase_words = phrase.split()
                pl = len(phrase_words)
                if i + pl <= len(words) and words[i:i+pl] == phrase_words:
                    result_parts.append(f"{{{dict_key}}}")
                    i += pl
                    matched = True
                    break
            if not matched:
                result_parts.append(words[i])
                i += 1
        
        compressed.append(' '.join(result_parts))
    
    return compressed

def calculate_savings(original_messages, dictionary, compressed_messages):
    original_length = sum(len(msg) for msg in original_messages)
    dict_length = sum(len(phrase) for phrase in dictionary.values())
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
    
    dictionary = find_common_phrases(messages, min_length)
    compressed_messages = compress_messages(messages, dictionary)
    savings = calculate_savings(messages, dictionary, compressed_messages)
    
    print("DICT:")
    for key in sorted(dictionary.keys(), key=lambda x: int(x[1:])):
        print(f"  {key}={dictionary[key]}")
    
    print("COMPRESSED:")
    for msg in compressed_messages:
        print(f"  {msg}")
    
    print(f"Savings: {savings}%")

if __name__ == "__main__":
    main()