import json
import sys
import re

def calculate_caps_ratio(message):
    letters = [c for c in message if c.isalpha()]
    if not letters:
        return 0.0
    caps = sum(1 for c in letters if c.isupper())
    return caps / len(letters)

def count_links(message):
    # Count HTTP/HTTPS URLs
    links = re.findall(r'https?://\S+', message, re.IGNORECASE)
    return len(links)

def count_keyword_matches(message):
    # Common spam keywords
    keywords = ['buy', 'free', 'money', 'win', 'prize', 'offer', 'deal', 'sale', 'discount', 'urgent']
    message_lower = message.lower()
    matches = 0
    for keyword in keywords:
        if keyword in message_lower:
            matches += 1
    return matches

def main():
    # Read input
    config_line = input().strip()
    message = input().strip()
    
    # Parse configuration
    config = json.loads(config_line)
    
    # Calculate heuristics
    caps_ratio = calculate_caps_ratio(message)
    link_count = count_links(message)
    keyword_matches = count_keyword_matches(message)
    
    # Calculate scores for each heuristic
    caps_score = 0
    link_score = 0
    keyword_score = 0
    
    if 'caps_ratio' in config:
        caps_score = min(config['caps_ratio'], int(caps_ratio * config['caps_ratio']))
    
    if 'link_count' in config:
        link_score = min(config['link_count'], link_count * 10)  # Scale links appropriately
        if link_count > 0:
            link_score = config['link_count']  # Full points if any links found
    
    if 'keyword_match' in config:
        keyword_score = min(config['keyword_match'], keyword_matches * 20)  # Scale keywords
    
    # Calculate total score
    total_score = caps_score + link_score + keyword_score
    
    # Output results
    print(f"score: {total_score}")
    
    if 'caps_ratio' in config:
        caps_percent = int(caps_ratio * 100)
        print(f"caps_ratio: {caps_score}/{config['caps_ratio']} ({caps_percent}% caps)")
    
    if 'link_count' in config:
        print(f"link_count: {link_score}/{config['link_count']} ({link_count} links)")
    
    if 'keyword_match' in config:
        print(f"keyword_match: {keyword_score}/{config['keyword_match']} ({keyword_matches} matches)")

if __name__ == "__main__":
    main()